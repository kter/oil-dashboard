import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from dynamodb import get_all_records, get_latest_record, put_record, record_exists
from pdf_fetcher import fetch_available_pdfs
from pdf_parser import parse_pdf

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ENV = os.environ.get("ENV", "dev")
FRONTEND_DOMAIN = os.environ.get("FRONTEND_DOMAIN", "http://localhost:5173")

app = FastAPI(title="Oil Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_DOMAIN],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/v1/reserves")
def list_reserves():
    records = get_all_records()
    last_updated = records[-1]["date"] if records else None
    return {"data": records, "last_updated": last_updated}


@app.get("/v1/reserves/latest")
def latest_reserves():
    record = get_latest_record()
    if record is None:
        return {"data": None, "last_updated": None}
    return {"data": record, "last_updated": record["date"]}


@app.post("/v1/reserves/fetch")
def trigger_fetch():
    """Manually trigger PDF fetch and parse."""
    return _do_fetch()


def _do_fetch() -> dict:
    """Fetch PDFs, parse them, and store new records."""
    pdfs = fetch_available_pdfs(months_back=12)
    added = 0
    for url, content in pdfs:
        records = parse_pdf(content, url)
        for record in records:
            if not record_exists(record.date):
                put_record(record)
                added += 1
                logger.info("Added record for %s", record.date)
            else:
                logger.info("Record for %s already exists, skipping", record.date)
    return {"status": "ok", "records_added": added, "pdfs_processed": len(pdfs)}


# Lambda handler via Mangum
mangum_handler = Mangum(app)


def lambda_handler(event, context):
    """Lambda entry point.

    Handles both API Gateway events and EventBridge scheduled events.
    """
    # EventBridge scheduled event
    if event.get("source") == "aws.events":
        logger.info("Triggered by EventBridge schedule")
        result = _do_fetch()
        logger.info("Fetch result: %s", result)
        return result

    # API Gateway event
    return mangum_handler(event, context)

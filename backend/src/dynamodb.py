import os
from decimal import Decimal

import boto3

from models import ReserveRecord

def _get_table():
    table_name = os.environ.get("DYNAMODB_TABLE", "oil-reserves-dev")
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "ap-northeast-1"))
    return dynamodb.Table(table_name)


def put_record(record: ReserveRecord) -> None:
    """Write a reserve record to DynamoDB."""
    table = _get_table()
    item = {
        "date": record.date,
        "national_days": Decimal(str(record.national_days)),
        "private_days": Decimal(str(record.private_days)),
        "cooperative_days": Decimal(str(record.cooperative_days)),
        "total_days": Decimal(str(record.total_days)),
        "source_pdf": record.source_pdf,
        "fetched_at": record.fetched_at,
    }
    table.put_item(Item=item)


def get_all_records() -> list[dict]:
    """Scan all records from DynamoDB, sorted by date."""
    table = _get_table()
    response = table.scan()
    items = response.get("Items", [])

    # Handle pagination
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    # Convert Decimal to float and sort by date
    records = []
    for item in items:
        records.append({
            "date": item["date"],
            "national_days": float(item["national_days"]),
            "private_days": float(item["private_days"]),
            "cooperative_days": float(item["cooperative_days"]),
            "total_days": float(item["total_days"]),
        })
    records.sort(key=lambda r: r["date"])
    return records


def get_latest_record() -> dict | None:
    """Get the most recent record."""
    records = get_all_records()
    return records[-1] if records else None


def record_exists(date_str: str) -> bool:
    """Check if a record for the given date already exists."""
    table = _get_table()
    response = table.get_item(Key={"date": date_str})
    return "Item" in response

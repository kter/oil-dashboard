import base64
import json
import logging
import os
import re

import boto3

from models import ReserveRecord

logger = logging.getLogger(__name__)

BEDROCK_MODEL_ID = "anthropic.claude-sonnet-4-6"

PROMPT = """このPDFは日本の石油備蓄量データです。全データをJSONで抽出してください。

[{"date":"YYYY-MM-DD","national_days":数値,"private_days":数値,"cooperative_days":数値}, ...]

- dateは各エントリの「（〇月〇日時点）」の日付をISO形式で（年は令和換算: 令和1年=2019年）
- 国家備蓄・民間備蓄・産油国共同備蓄の日数を抽出（全角数字は半角に変換）
- 産油国共同備蓄がない場合は0
- JSON配列のみ返す（説明不要）"""


def parse_pdf(content: bytes, source_url: str) -> list[ReserveRecord]:
    """Parse an ENECHO oil reserves PDF using Amazon Bedrock (Claude).

    Sends the PDF directly to Claude via the Bedrock document API and extracts
    all daily reserve records as structured JSON.
    """
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "ap-northeast-1"),
    )
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": base64.b64encode(content).decode(),
                        },
                    },
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
    }

    model_id = os.environ.get("BEDROCK_MODEL_ID", BEDROCK_MODEL_ID)
    resp = client.invoke_model(modelId=model_id, body=json.dumps(body))
    text = json.loads(resp["body"].read())["content"][0]["text"].strip()

    # Strip markdown code fences if Claude wrapped the JSON
    if text.startswith("```"):
        text = re.sub(r"^```[^\n]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text.rstrip())

    try:
        items = json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(
            "Bedrock returned invalid JSON from %s: %s\nResponse: %s", source_url, e, text[:500]
        )
        return []

    records = []
    for item in items:
        try:
            record = ReserveRecord.create(
                date=item["date"],
                national_days=float(item["national_days"]),
                private_days=float(item["private_days"]),
                cooperative_days=float(item.get("cooperative_days", 0)),
                source_pdf=source_url,
            )
            records.append(record)
            logger.info(
                "Parsed: %s national=%.1f private=%.1f coop=%.1f",
                item["date"],
                item["national_days"],
                item["private_days"],
                item.get("cooperative_days", 0),
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.warning("Skipping malformed record %s: %s", item, e)

    return records

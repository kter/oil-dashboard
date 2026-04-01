import logging
import re
from io import BytesIO

import pdfplumber

from models import ReserveRecord

logger = logging.getLogger(__name__)

# Japanese era year mappings
ERA_PATTERNS = {
    "令和": 2018,  # 令和1年 = 2019, so base is 2018
    "平成": 1988,  # 平成1年 = 1989, so base is 1988
}


def parse_japanese_date(text: str) -> str | None:
    """Parse Japanese era date like '令和7年2月末' to ISO date 'YYYY-MM-DD'.

    Returns the last day of the month.
    """
    for era, base_year in ERA_PATTERNS.items():
        match = re.search(rf"{era}\s*(\d+)\s*年\s*(\d+)\s*月", text)
        if match:
            year = base_year + int(match.group(1))
            month = int(match.group(2))
            # Get last day of month
            if month == 12:
                next_month_year = year + 1
                next_month = 1
            else:
                next_month_year = year
                next_month = month + 1
            from datetime import date, timedelta

            last_day = date(next_month_year, next_month, 1) - timedelta(days=1)
            return last_day.isoformat()
    return None


def extract_number(text: str) -> float | None:
    """Extract a numeric value from text, handling Japanese number formatting."""
    if not text:
        return None
    # Remove commas, spaces, and other non-numeric chars except dots
    cleaned = re.sub(r"[^\d.]", "", text.strip())
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_pdf(content: bytes, source_url: str) -> list[ReserveRecord]:
    """Parse an ENECHO oil reserves PDF and extract reserve data.

    The PDF contains a table with rows for different reserve types:
    - 国家備蓄 (National reserves)
    - 民間備蓄 (Private reserves)
    - 産油国共同備蓄 / 産油国協力備蓄 (Cooperative reserves)

    Each row contains reserve amounts in various units, including days (日数).
    """
    records: list[ReserveRecord] = []

    try:
        pdf = pdfplumber.open(BytesIO(content))
    except Exception as e:
        logger.error("Failed to open PDF: %s", e)
        return records

    data_date = None
    national_days = None
    private_days = None
    cooperative_days = None

    try:
        for page in pdf.pages:
            text = page.extract_text() or ""

            # Try to extract date from page text
            if not data_date:
                data_date = parse_japanese_date(text)

            # Extract tables
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row:
                        continue
                    row_text = " ".join(cell or "" for cell in row)

                    # Look for reserve type rows and extract days column
                    if "国家備蓄" in row_text and "民間" not in row_text:
                        national_days = _extract_days_from_row(row)
                    elif "民間備蓄" in row_text:
                        private_days = _extract_days_from_row(row)
                    elif "産油国" in row_text and ("共同" in row_text or "協同" in row_text or "協力" in row_text or "協働" in row_text):
                        cooperative_days = _extract_days_from_row(row)
    finally:
        pdf.close()

    if data_date and national_days is not None and private_days is not None:
        # Cooperative reserves may be 0 or missing for some periods
        coop = cooperative_days if cooperative_days is not None else 0.0
        record = ReserveRecord.create(
            date=data_date,
            national_days=national_days,
            private_days=private_days,
            cooperative_days=coop,
            source_pdf=source_url,
        )
        records.append(record)
        logger.info("Parsed record: date=%s, national=%.1f, private=%.1f, coop=%.1f", data_date, national_days, private_days, coop)
    else:
        logger.warning(
            "Incomplete data from %s: date=%s, national=%s, private=%s, coop=%s",
            source_url, data_date, national_days, private_days, cooperative_days,
        )

    return records


def _extract_days_from_row(row: list[str | None]) -> float | None:
    """Extract the days value from a table row.

    The days column is typically the last numeric column in the row.
    We look for values that are reasonable day counts (1-500).
    """
    candidates: list[float] = []
    for cell in reversed(row):
        val = extract_number(cell)
        if val is not None and 1 <= val <= 500:
            candidates.append(val)
            if len(candidates) >= 3:
                break

    # The days value is usually a relatively small number (< 300)
    # compared to volume numbers (tens of thousands)
    for val in candidates:
        if val < 300:
            return val

    return candidates[0] if candidates else None

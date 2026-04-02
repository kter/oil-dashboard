import logging
from datetime import date, timedelta

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl001/pdf-oil-res"
REQUEST_TIMEOUT = 30
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def find_latest_pdf_url(max_days_back: int = 30) -> str | None:
    """Find the latest available PDF by trying dates backward with HEAD requests.

    The latest PDF uses MMDD.pdf filename format.
    """
    today = date.today()
    for offset in range(max_days_back):
        d = today - timedelta(days=offset)
        filename = d.strftime("%m%d") + ".pdf"
        url = f"{BASE_URL}/{filename}"
        try:
            response = requests.head(
                url, timeout=REQUEST_TIMEOUT, allow_redirects=True, headers=HEADERS
            )
            if response.status_code == 200:
                logger.info("Found latest PDF: %s", url)
                return url
        except requests.RequestException as e:
            logger.debug("HEAD request failed for %s: %s", url, e)
            continue
    logger.warning("No PDF found within %d days", max_days_back)
    return None


def get_historical_pdf_urls(months_back: int = 12) -> list[str]:
    """Get URLs for historical monthly PDFs.

    Historical PDFs use YYMM.pdf filename format.
    """
    urls = []
    today = date.today()
    for offset in range(months_back):
        d = date(today.year, today.month, 1)
        month = d.month - offset
        year = d.year
        while month <= 0:
            month += 12
            year -= 1
        filename = f"{year % 100:02d}{month:02d}.pdf"
        url = f"{BASE_URL}/{filename}"
        urls.append(url)
    return urls


def check_url_exists(url: str) -> bool:
    """Check if a URL exists via HEAD request."""
    try:
        response = requests.head(
            url, timeout=REQUEST_TIMEOUT, allow_redirects=True, headers=HEADERS
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def download_pdf(url: str) -> bytes | None:
    """Download a PDF and return its content."""
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error("Failed to download %s: %s", url, e)
        return None


def fetch_available_pdfs(months_back: int = 12) -> list[tuple[str, bytes]]:
    """Fetch all available PDFs (latest + historical).

    Returns list of (url, content) tuples.
    """
    results: list[tuple[str, bytes]] = []

    # Try latest (MMDD format)
    latest_url = find_latest_pdf_url()
    if latest_url:
        content = download_pdf(latest_url)
        if content:
            results.append((latest_url, content))

    # Try historical (YYMM format)
    for url in get_historical_pdf_urls(months_back):
        if check_url_exists(url):
            content = download_pdf(url)
            if content:
                results.append((url, content))

    return results

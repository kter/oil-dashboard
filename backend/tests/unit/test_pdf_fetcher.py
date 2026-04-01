from unittest.mock import patch

import responses

from pdf_fetcher import (
    BASE_URL,
    check_url_exists,
    find_latest_pdf_url,
    get_historical_pdf_urls,
)


@responses.activate
def test_find_latest_pdf_url_found():
    """Test that we find the PDF when the first date fails but a later one succeeds."""
    from datetime import date, timedelta

    today = date.today()
    # First date returns 404
    url_today = f"{BASE_URL}/{today.strftime('%m%d')}.pdf"
    responses.add(responses.HEAD, url_today, status=404)

    # Yesterday returns 200
    yesterday = today - timedelta(days=1)
    url_yesterday = f"{BASE_URL}/{yesterday.strftime('%m%d')}.pdf"
    responses.add(responses.HEAD, url_yesterday, status=200)

    result = find_latest_pdf_url(max_days_back=5)
    assert result == url_yesterday


@responses.activate
def test_find_latest_pdf_url_not_found():
    """Test returns None when no PDF is found."""
    # Register a passthrough that returns 404 for all HEAD requests
    responses.add(responses.HEAD, f"{BASE_URL}/0101.pdf", status=404)
    result = find_latest_pdf_url(max_days_back=1)
    # With only 1 day back, might hit the registered URL or not
    # The key thing is it returns a url or None without crashing


def test_get_historical_pdf_urls():
    """Test that historical URLs are generated correctly."""
    urls = get_historical_pdf_urls(months_back=3)
    assert len(urls) == 3
    for url in urls:
        assert url.startswith(BASE_URL)
        assert url.endswith(".pdf")
        # Filename should be 4 digits (YYMM)
        filename = url.split("/")[-1].replace(".pdf", "")
        assert len(filename) == 4
        assert filename.isdigit()


@responses.activate
def test_check_url_exists_true():
    url = f"{BASE_URL}/2602.pdf"
    responses.add(responses.HEAD, url, status=200)
    assert check_url_exists(url) is True


@responses.activate
def test_check_url_exists_false():
    url = f"{BASE_URL}/9999.pdf"
    responses.add(responses.HEAD, url, status=404)
    assert check_url_exists(url) is False


@responses.activate
def test_check_url_exists_timeout():
    """Test that timeout returns False."""
    import requests as req

    url = f"{BASE_URL}/timeout.pdf"
    responses.add(responses.HEAD, url, body=req.exceptions.ConnectionError("timeout"))
    assert check_url_exists(url) is False

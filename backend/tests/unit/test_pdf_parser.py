import json
from unittest.mock import MagicMock, patch


def _make_bedrock_response(items: list) -> MagicMock:
    """Build a mock boto3 bedrock-runtime invoke_model response."""
    body_text = json.dumps(items)
    response_body = {
        "content": [{"type": "text", "text": body_text}],
    }
    mock_response = MagicMock()
    mock_response["body"].read.return_value = json.dumps(response_body).encode()
    return mock_response


def test_parse_pdf_single_record():
    """Parse PDF returns one record when Bedrock returns one entry."""
    from pdf_parser import parse_pdf

    items = [
        {"date": "2026-03-29", "national_days": 146, "private_days": 85, "cooperative_days": 5}
    ]
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = _make_bedrock_response(items)

    with patch("pdf_parser.boto3.client", return_value=mock_client):
        records = parse_pdf(b"%PDF-1.4 fake content", "https://example.com/0401.pdf")

    assert len(records) == 1
    r = records[0]
    assert r.date == "2026-03-29"
    assert r.national_days == 146.0
    assert r.private_days == 85.0
    assert r.cooperative_days == 5.0
    assert r.total_days == 236.0
    assert r.source_pdf == "https://example.com/0401.pdf"


def test_parse_pdf_multiple_records():
    """Parse PDF returns all records when Bedrock returns multiple entries."""
    from pdf_parser import parse_pdf

    items = [
        {"date": "2026-03-28", "national_days": 145, "private_days": 84, "cooperative_days": 5},
        {"date": "2026-03-29", "national_days": 146, "private_days": 85, "cooperative_days": 5},
        {"date": "2026-03-31", "national_days": 147, "private_days": 86, "cooperative_days": 5},
    ]
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = _make_bedrock_response(items)

    with patch("pdf_parser.boto3.client", return_value=mock_client):
        records = parse_pdf(b"%PDF fake", "https://example.com/0401.pdf")

    assert len(records) == 3
    assert records[0].date == "2026-03-28"
    assert records[2].national_days == 147.0


def test_parse_pdf_no_cooperative():
    """cooperative_days defaults to 0 when omitted."""
    from pdf_parser import parse_pdf

    items = [{"date": "2026-01-31", "national_days": 130, "private_days": 80}]
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = _make_bedrock_response(items)

    with patch("pdf_parser.boto3.client", return_value=mock_client):
        records = parse_pdf(b"%PDF fake", "https://example.com/0131.pdf")

    assert records[0].cooperative_days == 0.0


def test_parse_pdf_markdown_fence_stripped():
    """Bedrock response wrapped in markdown fences is handled correctly."""
    from pdf_parser import parse_pdf

    items = [
        {"date": "2026-03-29", "national_days": 146, "private_days": 85, "cooperative_days": 5}
    ]
    fenced = f"```json\n{json.dumps(items)}\n```"
    response_body = {"content": [{"type": "text", "text": fenced}]}
    mock_response = MagicMock()
    mock_response["body"].read.return_value = json.dumps(response_body).encode()
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = mock_response

    with patch("pdf_parser.boto3.client", return_value=mock_client):
        records = parse_pdf(b"%PDF fake", "https://example.com/0401.pdf")

    assert len(records) == 1


def test_parse_pdf_invalid_json_returns_empty():
    """Malformed JSON from Bedrock returns empty list without raising."""
    from pdf_parser import parse_pdf

    response_body = {
        "content": [{"type": "text", "text": "申し訳ありませんが、データが見つかりませんでした。"}]
    }
    mock_response = MagicMock()
    mock_response["body"].read.return_value = json.dumps(response_body).encode()
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = mock_response

    with patch("pdf_parser.boto3.client", return_value=mock_client):
        records = parse_pdf(b"%PDF fake", "https://example.com/broken.pdf")

    assert records == []

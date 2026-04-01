from models import ReserveRecord


def test_create_record():
    record = ReserveRecord.create(
        date="2026-02-28",
        national_days=133.0,
        private_days=85.0,
        cooperative_days=5.0,
        source_pdf="https://example.com/test.pdf",
    )
    assert record.date == "2026-02-28"
    assert record.national_days == 133.0
    assert record.private_days == 85.0
    assert record.cooperative_days == 5.0
    assert record.total_days == 223.0
    assert record.source_pdf == "https://example.com/test.pdf"
    assert record.fetched_at  # not empty


def test_to_dict():
    record = ReserveRecord.create(
        date="2026-02-28",
        national_days=133.0,
        private_days=85.0,
        cooperative_days=5.0,
        source_pdf="test.pdf",
    )
    d = record.to_dict()
    assert d["date"] == "2026-02-28"
    assert d["total_days"] == 223.0
    assert "fetched_at" in d


def test_to_api_response():
    record = ReserveRecord.create(
        date="2026-02-28",
        national_days=133.0,
        private_days=85.0,
        cooperative_days=5.0,
        source_pdf="test.pdf",
    )
    api = record.to_api_response()
    assert "date" in api
    assert "national_days" in api
    assert "fetched_at" not in api
    assert "source_pdf" not in api

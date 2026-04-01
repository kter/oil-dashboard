from pdf_parser import extract_number, parse_japanese_date


def test_parse_japanese_date_reiwa():
    assert parse_japanese_date("令和7年2月末現在") == "2025-02-28"
    assert parse_japanese_date("令和7年3月末") == "2025-03-31"
    assert parse_japanese_date("令和7年12月末") == "2025-12-31"
    assert parse_japanese_date("令和8年1月末") == "2026-01-31"


def test_parse_japanese_date_heisei():
    assert parse_japanese_date("平成31年3月末") == "2019-03-31"


def test_parse_japanese_date_no_match():
    assert parse_japanese_date("some random text") is None


def test_extract_number():
    assert extract_number("133") == 133.0
    assert extract_number("85.5") == 85.5
    assert extract_number("1,234") == 1234.0
    assert extract_number(" 42 ") == 42.0
    assert extract_number("") is None
    assert extract_number(None) is None


def test_extract_number_with_special_chars():
    assert extract_number("約133") == 133.0
    assert extract_number("133日") == 133.0

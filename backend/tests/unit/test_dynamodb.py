import os

import boto3
import pytest
from moto import mock_aws

from dynamodb import get_all_records, get_latest_record, put_record, record_exists
from models import ReserveRecord

TABLE_NAME = "oil-reserves-test"


@pytest.fixture(autouse=True)
def _setup_env(monkeypatch):
    monkeypatch.setenv("DYNAMODB_TABLE", TABLE_NAME)
    monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-northeast-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")


@pytest.fixture
def dynamodb_table(_setup_env):
    with mock_aws():
        client = boto3.client("dynamodb", region_name="ap-northeast-1")
        client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "date", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "date", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield


def _make_record(date: str, national: float = 133, private: float = 85, coop: float = 5):
    return ReserveRecord.create(
        date=date,
        national_days=national,
        private_days=private,
        cooperative_days=coop,
        source_pdf="test.pdf",
    )


def test_put_and_get_all(dynamodb_table):
    put_record(_make_record("2026-01-31"))
    put_record(_make_record("2026-02-28"))

    records = get_all_records()
    assert len(records) == 2
    assert records[0]["date"] == "2026-01-31"
    assert records[1]["date"] == "2026-02-28"


def test_get_latest(dynamodb_table):
    put_record(_make_record("2026-01-31"))
    put_record(_make_record("2026-02-28"))

    latest = get_latest_record()
    assert latest is not None
    assert latest["date"] == "2026-02-28"
    assert latest["national_days"] == 133.0


def test_get_latest_empty(dynamodb_table):
    assert get_latest_record() is None


def test_record_exists(dynamodb_table):
    assert record_exists("2026-01-31") is False
    put_record(_make_record("2026-01-31"))
    assert record_exists("2026-01-31") is True


def test_get_all_records_empty(dynamodb_table):
    assert get_all_records() == []

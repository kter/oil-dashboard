import os

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

TABLE_NAME = "oil-reserves-test"


@pytest.fixture(autouse=True)
def _setup_env(monkeypatch):
    monkeypatch.setenv("DYNAMODB_TABLE", TABLE_NAME)
    monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-northeast-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("FRONTEND_DOMAIN", "http://localhost:5173")


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        client = boto3.client("dynamodb", region_name="ap-northeast-1")
        client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "date", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "date", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield


@pytest.fixture
def client(dynamodb_table):
    from handler import app

    return TestClient(app)


def test_list_reserves_empty(client):
    response = client.get("/v1/reserves")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["last_updated"] is None


def test_list_reserves_with_data(client):
    # Insert test data directly
    from dynamodb import put_record
    from models import ReserveRecord

    record = ReserveRecord.create(
        date="2026-02-28",
        national_days=133.0,
        private_days=85.0,
        cooperative_days=5.0,
        source_pdf="test.pdf",
    )
    put_record(record)

    response = client.get("/v1/reserves")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["date"] == "2026-02-28"
    assert data["last_updated"] == "2026-02-28"


def test_latest_reserves_empty(client):
    response = client.get("/v1/reserves/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] is None


def test_latest_reserves_with_data(client):
    from dynamodb import put_record
    from models import ReserveRecord

    for month in ["01", "02"]:
        put_record(
            ReserveRecord.create(
                date=f"2026-{month}-28",
                national_days=130.0 + int(month),
                private_days=80.0 + int(month),
                cooperative_days=5.0,
                source_pdf="test.pdf",
            )
        )

    response = client.get("/v1/reserves/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["date"] == "2026-02-28"

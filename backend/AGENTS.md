# Backend - Agent Instructions

## Stack

- Python 3.12 + FastAPI on AWS Lambda (Docker)
- pdfplumber for PDF parsing
- boto3 for DynamoDB access
- Mangum as ASGI adapter for Lambda

## Commands

Prefer root `make` targets:

```bash
make be-test           # All backend tests
make be-test-unit      # Unit tests only
make be-test-integration # Integration tests
make be-lint           # Ruff linter
make be-format         # Ruff formatter
make be-format-check   # Ruff format check
make be-docker-build   # Build Docker image
```

## Conventions

- Use dataclasses for data models (`src/models.py`)
- PDF fetching uses HEAD requests for discovery before GET (`src/pdf_fetcher.py`)
- DynamoDB table: `oil-reserves-{env}`, partition key: `date` (YYYY-MM-DD)
- Lambda handler in `src/handler.py` with Mangum adapter
- Tests use `moto` for AWS service mocking, `responses` for HTTP mocking

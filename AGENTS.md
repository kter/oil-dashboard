# Oil Dashboard - Agent Instructions

## Overview

Japan oil reserves dashboard. Visualizes national (国家備蓄), private (民間備蓄), and cooperative (産油国協働備蓄) petroleum reserves from ENECHO/METI PDF data.

## Architecture

- **Frontend**: React + Vite + TypeScript SPA deployed to S3 + CloudFront
- **Backend**: Python 3.12 + FastAPI on AWS Lambda (Docker) + API Gateway + DynamoDB
- **Infrastructure**: Terraform with workspaces (dev/prd), separate AWS accounts
- **Domains**: Frontend: `oil.{dev.}devtools.site`, API: `api.oil.{dev.}devtools.site`

## Canonical Entry Point

The root `Makefile` is the canonical entry point for all project commands. Never run raw CLI commands when a `make` target exists.

## Tool Versions

All tool versions are managed via `mise.toml`. Run `mise install` to set up.

## Standard Commands

```bash
make setup              # Install all dependencies
make dev                # Start frontend dev server
make test               # Run all unit tests
make lint               # Run all linters
make format             # Format all code
make deploy ENV=dev     # Deploy to environment
make tf-plan ENV=dev    # Terraform plan
make tf-apply ENV=dev   # Terraform apply
make install-hooks      # Install git hooks via lefthook
```

## Conventions

- All user-facing text must use i18n (react-i18next). Support: ja, en, ko, zh-TW.
- Tests are required for every new feature and bug fix.
- Cross-stack operations run from repository root via `make` commands.
- Nested `AGENTS.md` files in subdirectories take precedence when conflicts occur.

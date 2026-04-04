.PHONY: setup setup-frontend setup-backend install-hooks \
	fe-dev fe-build fe-test fe-lint fe-format fe-format-check \
	be-test be-test-unit be-test-integration be-lint be-format be-format-check \
	be-docker-build be-docker-push \
	tf-init tf-plan tf-apply tf-fmt tf-validate tf-state-init \
	deploy deploy-frontend deploy-backend \
	lint format format-check test test-all \
	e2e-install e2e e2e-headed e2e-report \
	stop-hook-unit-tests claude-post-tool-use

# === Variables ===
ENV ?= dev
AWS_PROFILE := $(ENV)
AWS_REGION := ap-northeast-1
TF_DIR := terraform
FE_DIR := frontend
BE_DIR := backend

# Environment-specific settings
ifeq ($(ENV),prd)
  FRONTEND_DOMAIN := oil-dashboard.devtools.site
  API_DOMAIN := api.oil-dashboard.devtools.site
else
  FRONTEND_DOMAIN := oil-dashboard.dev.devtools.site
  API_DOMAIN := api.oil-dashboard.dev.devtools.site
endif

# === Setup ===
setup: setup-frontend setup-backend install-hooks

setup-frontend:
	cd $(FE_DIR) && npm install

setup-backend:
	cd $(BE_DIR) && uv sync

install-hooks:
	lefthook install

# === Frontend ===
fe-dev:
	cd $(FE_DIR) && VITE_API_URL=https://$(API_DOMAIN) npx vite

fe-build:
	cd $(FE_DIR) && VITE_API_URL=https://$(API_DOMAIN) npx vite build

fe-test:
	cd $(FE_DIR) && npx vitest run

fe-lint:
	cd $(FE_DIR) && npx eslint src/

fe-format:
	cd $(FE_DIR) && npx prettier --write "src/**/*.{ts,tsx,css}"

fe-format-check:
	cd $(FE_DIR) && npx prettier --check "src/**/*.{ts,tsx,css}"

# === Backend ===
be-test: be-test-unit

be-test-unit:
	cd $(BE_DIR) && uv run pytest tests/unit/ -v

be-test-integration:
	cd $(BE_DIR) && uv run pytest tests/integration/ -v

be-test-all:
	cd $(BE_DIR) && uv run pytest -v

be-lint:
	cd $(BE_DIR) && uv run ruff check src/ tests/

be-format:
	cd $(BE_DIR) && uv run ruff format src/ tests/

be-format-check:
	cd $(BE_DIR) && uv run ruff format --check src/ tests/

be-docker-build:
	cd $(BE_DIR) && docker build --platform linux/amd64 --provenance=false -t oil-dashboard-api:$(ENV) .

be-docker-push:
	$(eval ECR_REPO := $(shell AWS_PROFILE=$(AWS_PROFILE) aws ecr describe-repositories --repository-names oil-dashboard-api-$(ENV) --region $(AWS_REGION) --query 'repositories[0].repositoryUri' --output text))
	AWS_PROFILE=$(AWS_PROFILE) aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_REPO)
	docker tag oil-dashboard-api:$(ENV) $(ECR_REPO):latest
	docker push $(ECR_REPO):latest

# === Terraform ===
tf-init:
	cd $(TF_DIR) && AWS_PROFILE=$(AWS_PROFILE) terraform init -backend-config=backends/$(ENV).s3.tfbackend -reconfigure && terraform workspace select $(ENV) || terraform workspace new $(ENV)

tf-plan:
	cd $(TF_DIR) && AWS_PROFILE=$(AWS_PROFILE) terraform plan -var-file=envs/$(ENV).tfvars

tf-apply:
	cd $(TF_DIR) && AWS_PROFILE=$(AWS_PROFILE) terraform apply -var-file=envs/$(ENV).tfvars

tf-fmt:
	terraform -chdir=$(TF_DIR) fmt -recursive

tf-validate:
	cd $(TF_DIR) && terraform validate

tf-state-init:
	cd $(TF_DIR)/modules/state && terraform init && terraform workspace select $(ENV) || terraform workspace new $(ENV)
	cd $(TF_DIR)/modules/state && terraform apply -var="env=$(ENV)" -var="aws_profile=$(AWS_PROFILE)"

# === Deploy ===
deploy: deploy-backend deploy-frontend

deploy-backend: be-docker-build be-docker-push
	$(eval FUNCTION_NAME := oil-dashboard-api-$(ENV))
	AWS_PROFILE=$(AWS_PROFILE) aws lambda update-function-code \
		--function-name $(FUNCTION_NAME) \
		--image-uri $(shell AWS_PROFILE=$(AWS_PROFILE) aws ecr describe-repositories --repository-names oil-dashboard-api-$(ENV) --region $(AWS_REGION) --query 'repositories[0].repositoryUri' --output text):latest \
		--region $(AWS_REGION)

deploy-frontend: fe-build
	$(eval S3_BUCKET := oil-dashboard-frontend-$(ENV))
	AWS_PROFILE=$(AWS_PROFILE) aws s3 sync $(FE_DIR)/dist s3://$(S3_BUCKET) --delete --region $(AWS_REGION)
	$(eval CF_DIST_ID := $(shell AWS_PROFILE=$(AWS_PROFILE) aws cloudfront list-distributions --query "DistributionList.Items[?Aliases.Items[?contains(@,'$(FRONTEND_DOMAIN)')]].Id | [0]" --output text))
	AWS_PROFILE=$(AWS_PROFILE) aws cloudfront create-invalidation --distribution-id $(CF_DIST_ID) --paths "/*"

# === E2E (Playwright) ===
E2E_DIR := e2e

e2e-install:
	cd $(E2E_DIR) && npm install && npx playwright install chromium

e2e:
	cd $(E2E_DIR) && BASE_URL=https://$(FRONTEND_DOMAIN) npx playwright test

e2e-headed:
	cd $(E2E_DIR) && BASE_URL=https://$(FRONTEND_DOMAIN) npx playwright test --headed

e2e-report:
	cd $(E2E_DIR) && npx playwright show-report

# === Quality ===
lint: fe-lint be-lint tf-fmt

format: fe-format be-format tf-fmt

format-check: fe-format-check be-format-check

test: fe-test be-test-unit

test-all: fe-test be-test-all

# === Hooks ===
stop-hook-unit-tests: test

claude-post-tool-use:
	@if echo "$(FILE)" | grep -q "^frontend/"; then \
		cd $(FE_DIR) && npx prettier --write "$(patsubst frontend/%,%,$(FILE))" 2>/dev/null || true; \
	elif echo "$(FILE)" | grep -q "^backend/"; then \
		cd $(BE_DIR) && uv run ruff format "$(patsubst backend/%,%,$(FILE))" 2>/dev/null || true; \
	elif echo "$(FILE)" | grep -q "^terraform/.*\.tf$$"; then \
		terraform fmt "$(FILE)" 2>/dev/null || true; \
	fi

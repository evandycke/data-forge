PYTHON ?= python3
PROJECT_NAME := data-forge

install:
	$(PYTHON) -m pip install -e ".[dev]"
	pre-commit install

bootstrap:
	bootstrap-source-db

format:
	ruff format .
	mdformat README.md governance/openmetadata/README.md camel/README.md flyway/README.md

lint:
	ruff check .
	sqlfluff lint sql flyway/sql
	markdownlint-cli2 "**/*.md"

typecheck:
	mypy app pipelines scripts

test:
	pytest

run-api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-all:
	ingest-all

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

airflow-up:
	docker compose --profile airflow up -d airflow

camel-up:
	docker compose --profile camel up -d camel

openmetadata-bootstrap:
	bash scripts/bootstrap_openmetadata.sh

flyway-info:
	docker compose --profile flyway run --rm flyway info

flyway-validate:
	docker compose --profile flyway run --rm flyway validate

flyway-migrate:
	docker compose --profile flyway run --rm flyway migrate

from __future__ import annotations

from typing import Any

from pipelines.runners import (
    run_all_pipelines,
    run_api_pipeline,
    run_camel_json_pipeline,
    run_camel_text_pipeline,
    run_excel_pipeline,
    run_sql_database_pipeline,
    run_txt_pipeline,
)


def ingest_api() -> dict[str, Any]:
    return run_api_pipeline()


def ingest_txt() -> dict[str, Any]:
    return run_txt_pipeline()


def ingest_excel() -> dict[str, Any]:
    return run_excel_pipeline()


def ingest_database() -> dict[str, Any]:
    return run_sql_database_pipeline()


def ingest_all() -> dict[str, Any]:
    return run_all_pipelines()


def ingest_camel_text(payload: str, source_name: str) -> dict[str, Any]:
    return run_camel_text_pipeline(payload, source_name=source_name)


def ingest_camel_json(payload: dict[str, Any], source_name: str) -> dict[str, Any]:
    return run_camel_json_pipeline(payload, source_name=source_name)

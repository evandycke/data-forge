from __future__ import annotations

from typing import Any

from app.core.config import settings
from pipelines.common import build_pipeline, run_records_pipeline, serialize_load_info
from pipelines.sources.api_source import fetch_json_records
from pipelines.sources.excel_source import read_excel_records
from pipelines.sources.sql_source import build_sql_database_source
from pipelines.sources.txt_source import read_text_records


def run_api_pipeline(url: str | None = None) -> dict[str, Any]:
    pipeline_name = "api_ingestion"
    table_name = "api_users"
    records = fetch_json_records(url)

    info = run_records_pipeline(
        pipeline_name=pipeline_name,
        table_name=table_name,
        records=records,
        write_disposition="replace",
    )
    return serialize_load_info(
        info,
        pipeline_name=pipeline_name,
        table_name=table_name,
        details={"source": url or settings.sample_api_url, "record_count": len(records)},
    )


def run_txt_pipeline(file_path: str | None = None) -> dict[str, Any]:
    pipeline_name = "txt_ingestion"
    table_name = "txt_lines"
    effective_path = file_path or settings.sample_txt_path
    records = list(read_text_records(effective_path))

    info = run_records_pipeline(
        pipeline_name=pipeline_name,
        table_name=table_name,
        records=records,
        write_disposition="replace",
    )
    return serialize_load_info(
        info,
        pipeline_name=pipeline_name,
        table_name=table_name,
        details={"source_file": effective_path, "record_count": len(records)},
    )


def run_excel_pipeline(file_path: str | None = None) -> dict[str, Any]:
    pipeline_name = "excel_ingestion"
    table_name = "excel_rows"
    effective_path = file_path or settings.sample_excel_path
    records = list(read_excel_records(effective_path))

    info = run_records_pipeline(
        pipeline_name=pipeline_name,
        table_name=table_name,
        records=records,
        write_disposition="replace",
    )
    return serialize_load_info(
        info,
        pipeline_name=pipeline_name,
        table_name=table_name,
        details={"source_file": effective_path, "record_count": len(records)},
    )


def run_sql_database_pipeline(
    source_dsn: str | None = None,
    table_names: list[str] | None = None,
) -> dict[str, Any]:
    pipeline_name = "database_ingestion"
    effective_dsn = source_dsn or settings.source_db_dsn
    effective_tables = table_names or settings.source_db_table_list

    pipeline = build_pipeline(pipeline_name)
    source = build_sql_database_source(
        source_dsn=effective_dsn,
        table_names=effective_tables,
    )
    info = pipeline.run(source, write_disposition="replace")

    return serialize_load_info(
        info,
        pipeline_name=pipeline_name,
        table_name=",".join(effective_tables),
        details={"source_dsn": effective_dsn, "tables": effective_tables},
    )


def run_camel_text_pipeline(payload: str, source_name: str = "camel_file") -> dict[str, Any]:
    pipeline_name = "camel_text_ingestion"
    table_name = "camel_text_events"
    records = [{"source": source_name, "payload": payload.strip()}]

    info = run_records_pipeline(
        pipeline_name=pipeline_name,
        table_name=table_name,
        records=records,
        write_disposition="append",
    )
    return serialize_load_info(
        info,
        pipeline_name=pipeline_name,
        table_name=table_name,
        details={"source": source_name, "record_count": len(records)},
    )


def run_camel_json_pipeline(payload: dict[str, Any], source_name: str = "camel_api") -> dict[str, Any]:
    pipeline_name = "camel_json_ingestion"
    table_name = "camel_json_events"
    records = [{"source": source_name, **payload}]

    info = run_records_pipeline(
        pipeline_name=pipeline_name,
        table_name=table_name,
        records=records,
        write_disposition="append",
    )
    return serialize_load_info(
        info,
        pipeline_name=pipeline_name,
        table_name=table_name,
        details={"source": source_name, "record_count": len(records)},
    )


def run_all_pipelines() -> dict[str, Any]:
    return {
        "api": run_api_pipeline(),
        "txt": run_txt_pipeline(),
        "excel": run_excel_pipeline(),
        "database": run_sql_database_pipeline(),
    }

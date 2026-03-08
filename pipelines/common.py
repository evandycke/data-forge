from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import dlt
from dlt.destinations import postgres

from app.core.config import settings


def build_destination():
    return postgres(credentials=settings.postgres_dsn)


def build_pipeline(pipeline_name: str):
    return dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=build_destination(),
        dataset_name=settings.dlt_dataset,
    )


def run_records_pipeline(
    pipeline_name: str,
    table_name: str,
    records: Iterable[dict[str, Any]],
    write_disposition: str = "replace",
):
    pipeline = build_pipeline(pipeline_name)

    @dlt.resource(name=table_name, write_disposition=write_disposition)
    def records_resource():
        yield from records

    return pipeline.run(records_resource())


def serialize_load_info(
    info: Any,
    *,
    pipeline_name: str,
    table_name: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "status": "success",
        "pipeline_name": pipeline_name,
        "table_name": table_name,
        "dataset_name": settings.dlt_dataset,
        "summary": str(info),
        "details": details or {},
    }

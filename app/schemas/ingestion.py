from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class IngestionResponse(BaseModel):
    status: str
    pipeline_name: str
    table_name: str
    dataset_name: str
    summary: str
    details: dict[str, Any] | None = None

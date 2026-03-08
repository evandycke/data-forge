from __future__ import annotations

from pydantic import BaseModel


class QualityCheckResponse(BaseModel):
    status: str
    scan_name: str
    checks_group: str
    data_source_name: str
    configuration_path: str
    checks_path: str
    exit_code: int
    logs: str | None = None
    checks_summary: str | None = None
    failed_checks: str | None = None
    warn_or_fail_checks: str | None = None

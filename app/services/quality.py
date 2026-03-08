from __future__ import annotations

from typing import Any

from scripts.run_soda import run_soda_scan


def run_raw_quality_checks() -> dict[str, Any]:
    return run_soda_scan("raw_zone")


def run_analytics_quality_checks() -> dict[str, Any]:
    return run_soda_scan("analytics")

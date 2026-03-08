from __future__ import annotations

from typing import Any

from scripts.run_dbt import run_dbt_command


def run_dbt_build() -> dict[str, Any]:
    return run_dbt_command(["build"])

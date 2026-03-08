from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def dbt_paths() -> tuple[Path, Path, str]:
    root = project_root()
    project_dir = Path(os.getenv("DBT_PROJECT_DIR", root / "dbt")).resolve()
    profiles_dir = Path(os.getenv("DBT_PROFILES_DIR", project_dir / "profiles")).resolve()
    target = os.getenv("DBT_TARGET", "dev")
    return project_dir, profiles_dir, target


def build_dbt_command(cli_args: list[str] | None = None) -> list[str]:
    cli_args = cli_args or ["build"]
    project_dir, profiles_dir, target = dbt_paths()
    return [
        "dbt",
        *cli_args,
        "--project-dir",
        str(project_dir),
        "--profiles-dir",
        str(profiles_dir),
        "--target",
        target,
    ]


def run_dbt_command(cli_args: list[str] | None = None) -> dict[str, Any]:
    project_dir, profiles_dir, target = dbt_paths()
    command = build_dbt_command(cli_args)

    completed = subprocess.run(
        command,
        cwd=project_root(),
        capture_output=True,
        text=True,
        check=False,
    )

    return {
        "status": "success" if completed.returncode == 0 else "failed",
        "command": command,
        "project_dir": str(project_dir),
        "profiles_dir": str(profiles_dir),
        "target": target,
        "return_code": completed.returncode,
        "stdout": completed.stdout.strip() or None,
        "stderr": completed.stderr.strip() or None,
    }


def main() -> None:
    cli_args = sys.argv[1:] or ["build"]
    result = run_dbt_command(cli_args)

    if result["stdout"]:
        print(result["stdout"])

    if result["stderr"]:
        print(result["stderr"], file=sys.stderr)

    raise SystemExit(result["return_code"])

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from soda.scan import Scan

DEFAULT_GROUP_TO_DATA_SOURCE = {
    "raw_zone": "data_forge_raw",
    "analytics": "data_forge_analytics",
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def soda_paths() -> tuple[Path, Path]:
    root = project_root()
    configuration_path = Path(
        os.getenv("SODA_CONFIGURATION_PATH", root / "quality" / "soda" / "configuration.yml")
    ).resolve()
    checks_dir = Path(
        os.getenv("SODA_CHECKS_DIR", root / "quality" / "soda" / "checks")
    ).resolve()
    return configuration_path, checks_dir


def resolve_checks_path(checks_group: str) -> Path:
    _, checks_dir = soda_paths()
    checks_path = (checks_dir / checks_group).resolve()
    if not checks_path.exists():
        available_groups = sorted(
            path.name for path in checks_dir.iterdir() if path.is_dir()
        ) if checks_dir.exists() else []
        raise FileNotFoundError(
            f"Groupe de checks Soda introuvable: {checks_group}. "
            f"Groupes disponibles: {available_groups}"
        )
    return checks_path


def resolve_data_source_name(checks_group: str) -> str:
    env_var_name = f"SODA_{checks_group.upper()}_DATA_SOURCE_NAME"
    return os.getenv(
        env_var_name,
        DEFAULT_GROUP_TO_DATA_SOURCE.get(checks_group, checks_group),
    )


def run_soda_scan(
    checks_group: str,
    scan_name: str | None = None,
    *,
    fail_on_error: bool = False,
) -> dict[str, Any]:
    configuration_path, _ = soda_paths()
    checks_path = resolve_checks_path(checks_group)
    data_source_name = resolve_data_source_name(checks_group)
    resolved_scan_name = scan_name or f"data_forge_{checks_group}_scan"

    scan = Scan()
    scan.set_verbose(True)
    scan.set_is_local(True)
    scan.set_data_source_name(data_source_name)
    scan.set_scan_definition_name(resolved_scan_name)
    scan.add_configuration_yaml_file(str(configuration_path))
    scan.add_sodacl_yaml_files(str(checks_path))

    exit_code = scan.execute()
    logs = scan.get_logs_text()
    checks_summary = scan.get_all_checks_text()
    failed_checks = scan.get_checks_fail_text() if scan.has_check_fails() else None
    warn_or_fail = (
        scan.get_checks_warn_or_fail_text() if scan.has_checks_warn_or_fail() else None
    )

    status = "success"
    if exit_code == 1:
        status = "warning"
    elif exit_code != 0:
        status = "failed"

    result = {
        "status": status,
        "scan_name": resolved_scan_name,
        "checks_group": checks_group,
        "data_source_name": data_source_name,
        "configuration_path": str(configuration_path),
        "checks_path": str(checks_path),
        "exit_code": exit_code,
        "logs": logs.strip() or None,
        "checks_summary": checks_summary.strip() or None,
        "failed_checks": failed_checks.strip() if failed_checks else None,
        "warn_or_fail_checks": warn_or_fail.strip() if warn_or_fail else None,
    }

    if fail_on_error and exit_code != 0:
        raise RuntimeError(
            f"Le scan Soda {resolved_scan_name} a échoué avec le code {exit_code}.\n"
            f"{result['warn_or_fail_checks'] or result['logs'] or ''}"
        )

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Exécute un scan Soda local pour data-forge.")
    parser.add_argument(
        "checks_group",
        nargs="?",
        default="raw_zone",
        help="Groupe de checks Soda à exécuter (raw_zone, analytics, ...).",
    )
    parser.add_argument(
        "--scan-name",
        dest="scan_name",
        default=None,
        help="Nom logique du scan Soda.",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Retourne un code non nul si le scan émet un warning, un fail ou une erreur.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = run_soda_scan(
        checks_group=args.checks_group,
        scan_name=args.scan_name,
        fail_on_error=args.fail_on_error,
    )

    print(result["checks_summary"] or result["logs"] or "")
    raise SystemExit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()

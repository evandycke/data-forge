from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_quality_raw_route(monkeypatch) -> None:
    def fake_run_raw_quality_checks():
        return {
            "status": "success",
            "scan_name": "data_forge_raw_zone_scan",
            "checks_group": "raw_zone",
            "data_source_name": "data_forge_raw",
            "configuration_path": "quality/soda/configuration.yml",
            "checks_path": "quality/soda/checks/raw_zone",
            "exit_code": 0,
            "logs": None,
            "checks_summary": "all good",
            "failed_checks": None,
            "warn_or_fail_checks": None,
        }

    monkeypatch.setattr(
        "app.api.routes.run_raw_quality_checks",
        fake_run_raw_quality_checks,
    )

    client = TestClient(app)
    response = client.post("/quality/soda/raw")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["checks_group"] == "raw_zone"

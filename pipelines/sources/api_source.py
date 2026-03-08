from __future__ import annotations

from typing import Any

import requests

from app.core.config import settings


def fetch_json_records(url: str | None = None, timeout: int = 30) -> list[dict[str, Any]]:
    response = requests.get(url or settings.sample_api_url, timeout=timeout)
    response.raise_for_status()

    payload = response.json()
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        return [payload]

    raise TypeError("Le payload JSON récupéré ne peut pas être converti en enregistrements.")

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


def read_text_records(file_path: str) -> Iterator[dict[str, str | int]]:
    path = Path(file_path)
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue

        yield {
            "line_number": line_number,
            "text": line.strip(),
            "file_name": path.name,
        }

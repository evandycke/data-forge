# app/schemas/download.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class DownloadJob:
    key: str
    url: str
    target_dir: Path
    filename: Optional[str] = None
    headers: dict[str, str] = field(default_factory=dict)
    overwrite: bool = False
    expected_content_types: set[str] = field(default_factory=set)
    sha256: Optional[str] = None

@dataclass
class DownloadResult:
    key: str
    url: str
    path: str
    filename: str
    size_bytes: int
    sha256: str
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    status: str
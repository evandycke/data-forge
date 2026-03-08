from __future__ import annotations

from pydantic import BaseModel


class TransformationResponse(BaseModel):
    status: str
    command: list[str]
    project_dir: str
    profiles_dir: str
    target: str
    return_code: int
    stdout: str | None = None
    stderr: str | None = None

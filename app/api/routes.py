from __future__ import annotations

from fastapi import APIRouter, Body, Query, Request

from app.schemas.ingestion import IngestionResponse
from app.services.ingestion import (
    ingest_all,
    ingest_api,
    ingest_camel_json,
    ingest_camel_text,
    ingest_database,
    ingest_excel,
    ingest_txt,
)

router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/ingestions/api", response_model=IngestionResponse)
def ingest_api_route():
    return ingest_api()


@router.post("/ingestions/txt", response_model=IngestionResponse)
def ingest_txt_route():
    return ingest_txt()


@router.post("/ingestions/excel", response_model=IngestionResponse)
def ingest_excel_route():
    return ingest_excel()


@router.post("/ingestions/database", response_model=IngestionResponse)
def ingest_database_route():
    return ingest_database()


@router.post("/ingestions/all")
def ingest_all_route():
    return ingest_all()


@router.post("/camel/intake/text", response_model=IngestionResponse)
async def camel_text_intake(
    request: Request,
    source: str = Query(default="camel_file"),
):
    payload = (await request.body()).decode("utf-8")
    return ingest_camel_text(payload, source_name=source)


@router.post("/camel/intake/json", response_model=IngestionResponse)
def camel_json_intake(
    payload: dict = Body(...),
    source: str = Query(default="camel_api"),
):
    return ingest_camel_json(payload, source_name=source)

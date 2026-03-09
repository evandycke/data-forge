# app/catalog/download_catalog.py
from pathlib import Path
from app.models.download import DownloadJob

DOWNLOAD_CATALOG: dict[str, DownloadJob] = {
    "rpls_2025": DownloadJob(
        key="rpls_2025",
        url="https://www.data.gouv.fr/api/1/datasets/r/7649e51e-9418-4173-9dc6-cefb94bbd7c0",
        target_dir=Path("data/raw/rpls/2025"),
        filename="rpls_2025.csv",
        expected_content_types={"text/csv", "application/csv", "application/octet-stream"},
    ),
}
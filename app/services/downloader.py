# app/services/downloader.py
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import cgi

from app.models.download import DownloadJob, DownloadResult
from app.services.http_client import HttpClient

class FileDownloader:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def download(self, job: DownloadJob) -> DownloadResult:
        job.target_dir.mkdir(parents=True, exist_ok=True)

        with self.http_client.get_stream(job.url, headers=job.headers) as response:
            content_type = response.headers.get("content-type")
            etag = response.headers.get("etag")
            last_modified = response.headers.get("last-modified")

            if job.expected_content_types:
                if not content_type or not any(ct in content_type for ct in job.expected_content_types):
                    raise ValueError(
                        f"Content-Type inattendu: {content_type}, attendu parmi {sorted(job.expected_content_types)}"
                    )

            filename = job.filename or self._resolve_filename(response, job.url)
            target_path = job.target_dir / filename

            if target_path.exists() and not job.overwrite:
                return DownloadResult(
                    key=job.key,
                    url=job.url,
                    path=str(target_path),
                    filename=target_path.name,
                    size_bytes=target_path.stat().st_size,
                    sha256=self._sha256_file(target_path),
                    content_type=content_type,
                    etag=etag,
                    last_modified=last_modified,
                    status="already_present",
                )

            tmp_path = target_path.with_suffix(target_path.suffix + ".part")
            file_hash = hashlib.sha256()

            with open(tmp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    f.write(chunk)
                    file_hash.update(chunk)

            digest = file_hash.hexdigest()

            if job.sha256 and digest.lower() != job.sha256.lower():
                tmp_path.unlink(missing_ok=True)
                raise ValueError("Checksum SHA-256 invalide")

            tmp_path.replace(target_path)

        return DownloadResult(
            key=job.key,
            url=job.url,
            path=str(target_path),
            filename=target_path.name,
            size_bytes=target_path.stat().st_size,
            sha256=digest,
            content_type=content_type,
            etag=etag,
            last_modified=last_modified,
            status="downloaded",
        )

    @staticmethod
    def _resolve_filename(response, url: str) -> str:
        content_disposition = response.headers.get("content-disposition")
        if content_disposition:
            _, params = cgi.parse_header(content_disposition)
            if "filename" in params:
                return params["filename"]

        parsed = urlparse(url)
        candidate = Path(parsed.path).name
        return candidate or "downloaded_file"

    @staticmethod
    def _sha256_file(path: Path) -> str:
        file_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                file_hash.update(chunk)
        return file_hash.hexdigest()
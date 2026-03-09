# app/services/http_client.py
from dlt.sources.helpers import requests

class HttpClient:
    def __init__(self, timeout=(10, 300)) -> None:
        self.session = requests.Session(timeout=timeout, raise_for_status=True)

    def get_stream(self, url: str, headers: dict[str, str] | None = None):
        return self.session.get(url, headers=headers or {}, stream=True, allow_redirects=True)
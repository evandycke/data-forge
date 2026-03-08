from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "FastAPI dlt Lab"
    app_env: str = "dev"
    app_port: int = 8000

    dlt_dataset: str = "raw_zone"

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "raw_landing"
    postgres_user: str = "lab"
    postgres_password: str = "lab"

    sample_api_url: str = "https://jsonplaceholder.typicode.com/users"
    sample_txt_path: str = "data/sample.txt"
    sample_excel_path: str = "data/sample.xlsx"
    sample_camel_message_path: str = "data/camel_message.txt"

    source_db_path: str = "data/source.db"
    source_db_tables: str = "customers,orders"

    airflow_project_root: str = "/opt/airflow/project"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def source_db_dsn(self) -> str:
        resolved_path = Path(self.source_db_path).resolve()
        return f"sqlite:///{resolved_path}"

    @property
    def source_db_table_list(self) -> list[str]:
        return [table.strip() for table in self.source_db_tables.split(",") if table.strip()]

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

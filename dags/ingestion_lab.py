from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path("/opt/airflow/project")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from pipelines.runners import (
    run_api_pipeline,
    run_excel_pipeline,
    run_sql_database_pipeline,
    run_txt_pipeline,
)
from scripts.bootstrap_source_db import bootstrap_source_db

default_args = {
    "owner": "data-lab",
    "retries": 0,
}

with DAG(
    dag_id="data_lab_orchestration",
    default_args=default_args,
    description="Orchestration du bac à sable FastAPI + dlt + Camel",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["lab", "dlt", "fastapi", "camel"],
) as dag:
    bootstrap_db = PythonOperator(
        task_id="bootstrap_source_db",
        python_callable=bootstrap_source_db,
    )

    ingest_api = PythonOperator(
        task_id="ingest_api_data",
        python_callable=run_api_pipeline,
    )

    ingest_txt = PythonOperator(
        task_id="ingest_txt_data",
        python_callable=run_txt_pipeline,
    )

    ingest_excel = PythonOperator(
        task_id="ingest_excel_data",
        python_callable=run_excel_pipeline,
    )

    ingest_database = PythonOperator(
        task_id="ingest_database_data",
        python_callable=run_sql_database_pipeline,
    )

    drop_camel_file = BashOperator(
        task_id="drop_camel_file",
        bash_command=(
            "cp "
            "/opt/airflow/project/data/camel_message.txt "
            "/opt/airflow/project/camel/inbox/from_airflow.txt"
        ),
    )

    bootstrap_db >> [ingest_api, ingest_txt, ingest_excel, ingest_database, drop_camel_file]

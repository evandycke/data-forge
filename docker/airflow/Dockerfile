FROM apache/airflow:3.1.7-python3.12

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY pyproject.toml README.md /opt/airflow/project/
COPY app /opt/airflow/project/app
COPY pipelines /opt/airflow/project/pipelines
COPY scripts /opt/airflow/project/scripts
COPY data /opt/airflow/project/data

RUN pip install --no-cache-dir /opt/airflow/project

ENV PYTHONPATH=/opt/airflow/project
WORKDIR /opt/airflow/project

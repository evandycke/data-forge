# data-forge

Bac à sable prêt pour GitHub afin de tester :

- **FastAPI** pour exposer des endpoints de déclenchement,
- **dlt** pour les chargements vers PostgreSQL,
- **Apache Camel** pour des usages d'intégration complémentaires,
- **Apache Airflow** pour l'orchestration,
- **OpenMetadata** pour la gouvernance et le catalogage,
- **Flyway** pour versionner les modifications de structure PostgreSQL.

## Architecture cible

```text
API externes ─┐
TXT --------- ├─> FastAPI / scripts / Airflow / Camel ─> dlt ─> PostgreSQL
Excel ------- ┤
Base SQL -----┘

                                   ├─> Airflow : orchestration
                                   ├─> Flyway : migrations DDL PostgreSQL
                                   └─> OpenMetadata : gouvernance
```

## Ce que contient le dépôt

- `app/` : API FastAPI
- `pipelines/` : pipelines d'ingestion `dlt`
- `scripts/` : bootstrap et exécutions locales
- `dags/` : DAG Airflow
- `camel/` : routes Apache Camel YAML DSL
- `governance/openmetadata/` : brique OpenMetadata et documentation
- `flyway/` : migrations de schéma PostgreSQL
- `infra/postgres/` : initialisation PostgreSQL
- `sql/` : requêtes SQL d'exemple
- `.pre-commit-config.yaml` : hooks qualité

## Sources testées par le projet

- API JSON (`JSONPlaceholder` par défaut),
- fichier TXT,
- fichier Excel,
- base SQLite jouant le rôle de base source,
- événements injectés par Apache Camel.

## Démarrage local sans Docker

```bash
python -m venv .venv
source .venv/bin/activate
cp .env.example .env
python -m pip install -e ".[dev]"
pre-commit install
bootstrap-source-db
uvicorn app.main:app --reload
```

## Démarrage avec Docker

```bash
cp .env.example .env
docker compose up -d --build
```

Endpoints utiles :

- FastAPI : `http://localhost:8000/docs`
- Santé : `http://localhost:8000/health`

## Activer Airflow

```bash
docker compose --profile airflow up -d airflow
```

Le DAG fourni s'appelle `data_lab_orchestration`.

> Airflow ici est monté en **mode laboratoire** pour tester l'orchestration
> locale. Pour un usage réel, prévoyez une topologie plus robuste.

## Activer Apache Camel

```bash
docker compose --profile camel up -d camel
cp data/camel_message.txt camel/inbox/demo.txt
```

Le fichier déposé est routé par Camel vers FastAPI, puis chargé dans
PostgreSQL via `dlt`.

## Flyway

Appliquer les migrations de structure PostgreSQL :

```bash
docker compose up -d postgres
make flyway-info
make flyway-validate
make flyway-migrate
```

Flyway gère ici les schémas techniques (`data_forge_admin`, `raw_zone`,
`analytics`, `data_quality`) et les tables d'administration.

## OpenMetadata

Bootstrap de la stack officielle :

```bash
make openmetadata-bootstrap
```

Ensuite, suivez `governance/openmetadata/README.md`.

## Déclenchements disponibles

- `POST /ingestions/api`
- `POST /ingestions/txt`
- `POST /ingestions/excel`
- `POST /ingestions/database`
- `POST /ingestions/all`

## Pre-commit et qualité

Le projet inclut :

- **Python** : Ruff (lint + format)
- **SQL** : SQLFluff
- **Markdown** : mdformat + markdownlint-cli2
- hooks utilitaires : YAML/TOML, whitespace, merge conflicts

Installation :

```bash
pre-commit install
pre-commit run --all-files
```

## Commandes utiles

```bash
make bootstrap
make lint
make format
make test
make run-all
make airflow-up
make camel-up
make openmetadata-bootstrap
make flyway-info
make flyway-validate
make flyway-migrate
```

## Exemple de scénario de test

1. Initialiser la base source SQLite avec `make bootstrap`.
1. Démarrer PostgreSQL puis exécuter `make flyway-migrate`.
1. Démarrer FastAPI.
1. Appeler `POST /ingestions/all`.
1. Vérifier les tables et schémas dans PostgreSQL.
1. Activer Airflow pour orchestrer le même scénario.
1. Activer Camel pour déposer un fichier dans `camel/inbox/`.
1. Cataloguer la base cible et les pipelines dans OpenMetadata.

## Points d'extension évidents

- ajouter de vraies APIs métier,
- brancher une base source PostgreSQL/MySQL plutôt que SQLite,
- enrichir les DAGs Airflow avec notifications et contrôles,
- ajouter des migrations Flyway par domaine métier,
- publier la métadonnée technique et métier dans OpenMetadata,
- ajouter des tests d'intégration et une CI plus poussée.

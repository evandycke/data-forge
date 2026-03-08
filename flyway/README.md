# Flyway dans data-forge

Flyway gère ici les **évolutions de structure PostgreSQL** :

- création de schémas techniques,
- tables d'administration,
- futures évolutions DDL versionnées.

## Répartition des responsabilités

- **Flyway** : DDL, schémas, tables techniques, changements structurels versionnés
- **dlt** : ingestion et chargement des données
- **FastAPI / scripts / Airflow** : déclenchement et orchestration des traitements

## Fichiers clés

- `conf/flyway.toml` : configuration Flyway
- `sql/V*__*.sql` : migrations versionnées

## Commandes

```bash
docker compose up -d postgres
docker compose --profile flyway run --rm flyway info
docker compose --profile flyway run --rm flyway validate
docker compose --profile flyway run --rm flyway migrate
```

Avec le `Makefile` :

```bash
make flyway-info
make flyway-validate
make flyway-migrate
```

## Convention proposée

- `V1__...sql`, `V2__...sql` : migrations versionnées
- éviter les modifications manuelles directement en base
- exécuter Flyway avant les ingestions

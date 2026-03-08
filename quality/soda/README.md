# Soda dans data-forge

Ce dossier contient la configuration locale de `Soda Core` pour exécuter des
scans de qualité sur PostgreSQL :

- `configuration.yml` : deux data sources Soda, une pour `raw_zone`, une pour `analytics`
- `checks/raw_zone/` : contrôles après ingestion `dlt`
- `checks/analytics/` : contrôles après transformations `dbt`

Exemples :

```bash
make soda-test-connection
make soda-scan-raw
make soda-scan-analytics
```

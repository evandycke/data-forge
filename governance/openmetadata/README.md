# OpenMetadata

Cette brique couvre la gouvernance, le catalogage et la découverte des données
du bac à sable.

## Pourquoi ce montage est séparé

OpenMetadata fournit sa propre stack Docker et une configuration versionnée.
Pour garder le socle FastAPI + dlt + Airflow + Camel simple et maintenable,
le projet propose :

- un script de bootstrap pour récupérer le `docker-compose` officiel,
- un emplacement dédié `governance/openmetadata/`,
- une documentation d'intégration avec PostgreSQL et Airflow.

## Bootstrap

```bash
make openmetadata-bootstrap
```

Le script télécharge le `docker-compose-openmetadata.yml` officiel depuis
les releases OpenMetadata.

## Démarrage

Une fois le fichier récupéré et adapté :

```bash
docker compose -f governance/openmetadata/docker-compose-openmetadata.yml up -d
```

## Intégration suggérée avec ce projet

- **Base PostgreSQL cible** : déclarez `raw_landing` comme service de base
de données à cataloguer.
- **Pipelines Airflow** : utilisez Airflow comme orchestrateur de workflows
d'ingestion.
- **Documentation / ownership / classification** : créez les descriptions,
propriétaires, tags et classifications dans OpenMetadata.

## Point d'attention

Le fichier récupéré reste celui de l'éditeur OpenMetadata.
Gardez la même version entre :

- le serveur OpenMetadata,
- les packages d'ingestion OpenMetadata,
- les éventuelles intégrations Airflow.

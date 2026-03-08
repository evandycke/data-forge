# Apache Camel

Cette brique sert à tester des patterns d'intégration complémentaires
au code Python :

- surveillance d'un répertoire de dépôt,
- routage de contenu brut vers FastAPI,
- enrichissement ou transformation légère avant chargement.

## Route fournie

La route `routes/file_to_fastapi.camel.yaml` :

1. surveille `camel/inbox/`,
2. lit les fichiers `*.txt`,
3. envoie leur contenu vers `POST /camel/intake/text`,
4. délègue ensuite le chargement dans PostgreSQL à `dlt`.

## Démarrage

Le service est déjà décrit dans `docker-compose.yml` sous le profil `camel`.

```bash
docker compose --profile camel up -d camel
```

Pour tester :

```bash
cp data/camel_message.txt camel/inbox/demo.txt
```

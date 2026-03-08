#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/governance/openmetadata"
RELEASE_TAG="${OPENMETADATA_RELEASE_TAG:-1.12.1-release}"

mkdir -p "${TARGET_DIR}"

echo "Téléchargement du docker-compose officiel OpenMetadata (${RELEASE_TAG})..."
curl -fsSL \
  "https://github.com/open-metadata/OpenMetadata/releases/download/${RELEASE_TAG}/docker-compose-openmetadata.yml" \
  -o "${TARGET_DIR}/docker-compose-openmetadata.yml"

cat > "${TARGET_DIR}/.env.example" <<'EOF'
# Variables minimales à adapter selon votre environnement OpenMetadata.
# Référez-vous à la documentation officielle OpenMetadata pour la liste complète.
OPENMETADATA_SERVER_PORT=8585
OPENMETADATA_RELEASE_TAG=1.12.1-release
EOF

echo "Fichier généré : ${TARGET_DIR}/docker-compose-openmetadata.yml"
echo "Consultez ${TARGET_DIR}/README.md pour la suite."

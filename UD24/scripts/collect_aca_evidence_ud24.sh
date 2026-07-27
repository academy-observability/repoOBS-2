#!/usr/bin/env bash
set -euo pipefail
RESOURCE_GROUP="${RESOURCE_GROUP:-}"
FRONTEND_APP="${FRONTEND_APP:-}"
BACKEND_APP="${BACKEND_APP:-}"
OUT_DIR="${1:-UD24/logs}"
mkdir -p "$OUT_DIR"

if [[ -z "$RESOURCE_GROUP" || -z "$FRONTEND_APP" || -z "$BACKEND_APP" ]]; then
  echo "Imposta RESOURCE_GROUP, FRONTEND_APP, BACKEND_APP" >&2
  exit 1
fi

az containerapp show --resource-group "$RESOURCE_GROUP" --name "$FRONTEND_APP" -o json > "$OUT_DIR/frontend_containerapp.json"
az containerapp show --resource-group "$RESOURCE_GROUP" --name "$BACKEND_APP" -o json > "$OUT_DIR/backend_containerapp.json"
az containerapp revision list --resource-group "$RESOURCE_GROUP" --name "$FRONTEND_APP" -o json > "$OUT_DIR/frontend_revisions.json"
az containerapp revision list --resource-group "$RESOURCE_GROUP" --name "$BACKEND_APP" -o json > "$OUT_DIR/backend_revisions.json"

echo "Evidenze ACA salvate in $OUT_DIR"

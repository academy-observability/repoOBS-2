#!/usr/bin/env bash
set -euo pipefail

: "${RG:?Impostare RG}"
: "${BACKEND_APP:?Impostare BACKEND_APP}"
: "${FRONTEND_APP:?Impostare FRONTEND_APP}"
# ENV_NAME è opzionale: eliminare l'ambiente solo se non serve ad altre app.

az containerapp delete --resource-group "$RG" --name "$FRONTEND_APP" --yes || true
az containerapp delete --resource-group "$RG" --name "$BACKEND_APP" --yes || true

if [[ -n "${ENV_NAME:-}" ]]; then
  echo "Eliminazione ambiente ACA: $ENV_NAME"
  az containerapp env delete --resource-group "$RG" --name "$ENV_NAME" --yes || true
else
  echo "Ambiente ACA non eliminato. Impostare ENV_NAME per eliminarlo consapevolmente."
fi

#!/usr/bin/env bash
set -euo pipefail

: "${RG:?Impostare RG}"
: "${BACKEND_APP:?Impostare BACKEND_APP}"
: "${FRONTEND_APP:?Impostare FRONTEND_APP}"

az containerapp show --resource-group "$RG" --name "$BACKEND_APP" \
  --query "{name:name,provisioningState:properties.provisioningState,fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName}" \
  -o json

az containerapp show --resource-group "$RG" --name "$FRONTEND_APP" \
  --query "{name:name,provisioningState:properties.provisioningState,fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName}" \
  -o json

FRONTEND_FQDN=$(az containerapp show --resource-group "$RG" --name "$FRONTEND_APP" --query properties.configuration.ingress.fqdn -o tsv)
echo "Frontend URL: https://${FRONTEND_FQDN}"
curl -i "https://${FRONTEND_FQDN}/health"
curl -i "https://${FRONTEND_FQDN}/ready"

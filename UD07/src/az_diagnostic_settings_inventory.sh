#!/usr/bin/env bash
set -euo pipefail

# UD07 - Esporta Diagnostic Settings e categorie diagnostiche di una risorsa Azure.
# Uso:
#   bash src/az_diagnostic_settings_inventory.sh "$RESOURCE_ID" [settings_output] [categories_output]

RESOURCE_ID="${1:-}"
SETTINGS_OUTPUT="${2:-evidence/diagnostic_settings.json}"
CATEGORIES_OUTPUT="${3:-evidence/diagnostic_categories.json}"

if [[ -z "$RESOURCE_ID" ]]; then
  echo "Uso: $0 <RESOURCE_ID> [settings_output] [categories_output]" >&2
  exit 1
fi

mkdir -p evidence logs "$(dirname "$SETTINGS_OUTPUT")" "$(dirname "$CATEGORIES_OUTPUT")"

echo "== Diagnostic Settings esistenti =="
az monitor diagnostic-settings list \
  --resource "$RESOURCE_ID" \
  --output json > "$SETTINGS_OUTPUT"

echo "File creato: $SETTINGS_OUTPUT"

az monitor diagnostic-settings list \
  --resource "$RESOURCE_ID" \
  --query '[].{name:name, workspace:workspaceId, storage:storageAccountId, eventHub:eventHubAuthorizationRuleId}' \
  --output table || true

echo "== Categorie diagnostiche disponibili =="
az monitor diagnostic-settings categories list \
  --resource "$RESOURCE_ID" \
  --output json > "$CATEGORIES_OUTPUT"

echo "File creato: $CATEGORIES_OUTPUT"

az monitor diagnostic-settings categories list \
  --resource "$RESOURCE_ID" \
  --output table || true

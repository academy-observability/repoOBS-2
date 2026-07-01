#!/usr/bin/env bash
set -euo pipefail

# UD07 - Esporta definizioni metriche di una risorsa Azure.
# Uso:
#   bash src/az_metric_definitions.sh "$RESOURCE_ID" [output_file]
# Esempio:
#   bash src/az_metric_definitions.sh "$APP_ID" evidence/ud07_appservice_metric_definitions.json

RESOURCE_ID="${1:-}"
OUTPUT_FILE="${2:-evidence/metric_definitions.json}"

if [[ -z "$RESOURCE_ID" ]]; then
  echo "Uso: $0 <RESOURCE_ID> [output_file]" >&2
  exit 1
fi

mkdir -p evidence logs "$(dirname "$OUTPUT_FILE")"

echo "== Definizioni metriche =="
echo "Risorsa: $RESOURCE_ID"

az monitor metrics list-definitions \
  --resource "$RESOURCE_ID" \
  --output json > "$OUTPUT_FILE"

echo "File creato: $OUTPUT_FILE"

az monitor metrics list-definitions \
  --resource "$RESOURCE_ID" \
  --query '[].{name:name.value, display:displayName, unit:unit, primaryAggregation:primaryAggregationType}' \
  --output table || true

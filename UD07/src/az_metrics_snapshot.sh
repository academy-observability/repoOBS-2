#!/usr/bin/env bash
set -euo pipefail

# UD07 - Esporta valori metrici recenti di una risorsa Azure.
# Uso:
#   bash src/az_metrics_snapshot.sh "$RESOURCE_ID" "Requests" PT1M Total evidence/requests.json
# Parametri:
#   $1 RESOURCE_ID
#   $2 METRIC_NAME
#   $3 INTERVAL, per esempio PT1M o PT5M
#   $4 AGGREGATION, per esempio Total oppure "Average Maximum"
#   $5 OUTPUT_FILE

RESOURCE_ID="${1:-}"
METRIC_NAME="${2:-}"
INTERVAL="${3:-PT1M}"
AGGREGATION="${4:-Average Maximum Total Count}"
OUTPUT_FILE="${5:-evidence/metric_values.json}"

if [[ -z "$RESOURCE_ID" || -z "$METRIC_NAME" ]]; then
  echo "Uso: $0 <RESOURCE_ID> <METRIC_NAME> [INTERVAL] [AGGREGATION] [OUTPUT_FILE]" >&2
  exit 1
fi

mkdir -p evidence logs "$(dirname "$OUTPUT_FILE")"

echo "== Snapshot metrica =="
echo "Risorsa: $RESOURCE_ID"
echo "Metrica: $METRIC_NAME"
echo "Interval/granularità: $INTERVAL"
echo "Aggregazione: $AGGREGATION"
echo "Nota: --interval indica la granularità dei punti restituiti, non il time range complessivo."

az monitor metrics list \
  --resource "$RESOURCE_ID" \
  --metric "$METRIC_NAME" \
  --interval "$INTERVAL" \
  --aggregation $AGGREGATION \
  --output json > "$OUTPUT_FILE"

echo "File creato: $OUTPUT_FILE"

if command -v jq >/dev/null 2>&1; then
  jq '.value[0].name, .value[0].timeseries[0].data[0:5]' "$OUTPUT_FILE" || true
else
  echo "Anteprima alternativa: python3 -m json.tool $OUTPUT_FILE | head -80"
fi

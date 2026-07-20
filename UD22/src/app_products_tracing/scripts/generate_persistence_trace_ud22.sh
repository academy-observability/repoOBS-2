#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8122}"
mkdir -p ../../evidence
REQUEST_ID="ud22-persistence-$(date +%s)-$RANDOM"
RESPONSE="$(curl -sS -H "X-Request-Id: ${REQUEST_ID}" "${FRONTEND_URL}/products/slow")"
TRACE_ID="$(printf '%s' "$RESPONSE" | python -c 'import json,sys; print(json.load(sys.stdin).get("trace_id", ""))')"
printf '%s\n' "$TRACE_ID" > ../../evidence/persistence_trace_id_ud22.txt
printf '%s\n' "$REQUEST_ID" > ../../evidence/persistence_request_id_ud22.txt

echo "Trace di persistenza generata"
echo "request_id=${REQUEST_ID}"
echo "trace_id=${TRACE_ID}"
echo "Jaeger: http://localhost:16686/trace/${TRACE_ID}"
echo "Identificatore salvato in ../../evidence/persistence_trace_id_ud22.txt"

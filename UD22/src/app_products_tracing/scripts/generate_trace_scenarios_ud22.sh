#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
FRONTEND_URL="${FRONTEND_URL:-http://localhost:8122}"
mkdir -p ../../evidence
OUT="../../evidence/trace_scenarios_ud22.txt"
: > "$OUT"

run_case() {
  local label="$1"
  local path="$2"
  local request_id="ud22-${label}-$(date +%s)-$RANDOM"
  local response
  response="$(curl -sS -H "X-Request-Id: ${request_id}" "${FRONTEND_URL}${path}")"
  local trace_id
  trace_id="$(printf '%s' "$response" | python -c 'import json,sys; print(json.load(sys.stdin).get("trace_id", ""))')"
  printf '%-8s request_id=%s\n' "$label" "$request_id"
  printf '         trace_id=%s\n' "$trace_id"
  printf '         Jaeger: http://localhost:16686/trace/%s\n' "$trace_id"
  printf '%s|%s|%s|%s\n' "$label" "$path" "$request_id" "$trace_id" >> "$OUT"
  sleep 1
}

echo "Generazione di tre trace controllate"
run_case normal /products
run_case slow /products/slow
run_case error /products/error

echo
echo "Identificatori salvati in: $OUT"
echo "Attendere alcuni secondi per l'esportazione batch, quindi aprire Jaeger."

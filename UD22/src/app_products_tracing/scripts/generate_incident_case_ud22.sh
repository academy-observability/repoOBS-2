#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
FRONTEND_URL="${FRONTEND_URL:-http://localhost:8122}"
STAMP="$(date +%s)"
mkdir -p ../../evidence
OUT="../../evidence/incident_case_request_ids_ud22.txt"
: > "$OUT"

paths=(
  /products
  /products
  /products/slow
  /products
  /products
  /products/error
  /products
  /products
)

echo "Generazione caso di indagine: 8 richieste"
for i in $(seq 1 8); do
  rid="ud22-case-$(printf '%02d' "$i")-${STAMP}"
  path="${paths[$((i-1))]}"
  curl -sS -H "X-Request-Id: ${rid}" "${FRONTEND_URL}${path}" >/dev/null || true
  echo "$rid" | tee -a "$OUT"
  sleep 1
done

echo
echo "Usare Jaeger e i log per individuare la richiesta lenta e quella in errore."
echo "Elenco salvato in $OUT"

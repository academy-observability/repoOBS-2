#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8121}"
DURATION_SECONDS="${DURATION_SECONDS:-60}"
SLEEP_SECONDS="${SLEEP_SECONDS:-0.20}"

end=$((SECONDS + DURATION_SECONDS))
echo "Genero baseline normale UD21 per circa ${DURATION_SECONDS}s verso ${FRONTEND_URL}"
echo "Endpoint: /, /products, /ready. Nessun /products/error o /products/slow."

while (( SECONDS < end )); do
  curl -fsS -o /dev/null "${FRONTEND_URL}/" || true
  curl -fsS -o /dev/null "${FRONTEND_URL}/products" || true
  curl -fsS -o /dev/null "${FRONTEND_URL}/ready" || true
  sleep "$SLEEP_SECONDS"
done

echo "Baseline completata. Error rate atteso: circa 0."

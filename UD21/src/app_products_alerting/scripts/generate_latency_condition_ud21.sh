#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8121}"
DURATION_SECONDS="${DURATION_SECONDS:-180}"
SLEEP_SECONDS="${SLEEP_SECONDS:-0.10}"

end=$((SECONDS + DURATION_SECONDS))
echo "Genero latency burst UD21 per circa ${DURATION_SECONDS}s"
echo "Endpoint: /products e /products/slow."

while (( SECONDS < end )); do
  curl -s -o /dev/null "${FRONTEND_URL}/products" || true
  curl -s -o /dev/null "${FRONTEND_URL}/products/slow" || true
  sleep "$SLEEP_SECONDS"
done

echo "Latency burst terminato."

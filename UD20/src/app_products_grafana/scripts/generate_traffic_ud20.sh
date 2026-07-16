#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8120}"
ROUNDS="${ROUNDS:-60}"
SLEEP_SECONDS="${SLEEP_SECONDS:-0.25}"

echo "Genero traffico UD20 verso ${FRONTEND_URL}"
echo "Round: ${ROUNDS}"

echo "Traffico normale, lento e con errori controllati."
for i in $(seq 1 "$ROUNDS"); do
  curl -s -o /dev/null "${FRONTEND_URL}/" || true
  curl -s -o /dev/null "${FRONTEND_URL}/products" || true
  if (( i % 4 == 0 )); then
    curl -s -o /dev/null "${FRONTEND_URL}/ready" || true
  fi
  if (( i % 5 == 0 )); then
    curl -s -o /dev/null "${FRONTEND_URL}/products/slow" || true
  fi
  if (( i % 8 == 0 )); then
    curl -s -o /dev/null "${FRONTEND_URL}/products/error" || true
  fi
  sleep "$SLEEP_SECONDS"
done

echo "Traffico completato. Aprire Grafana: http://localhost:3000 admin/admin"
echo "Dashboard: Academy Observability / UD20 - Catalogo prodotti - FE/BE metrics"

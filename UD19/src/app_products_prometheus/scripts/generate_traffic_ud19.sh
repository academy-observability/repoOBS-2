#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8118}"
ROUNDS="${ROUNDS:-30}"

echo "Genero traffico applicativo verso ${FRONTEND_URL}"
echo "Round: ${ROUNDS}"

for i in $(seq 1 "$ROUNDS"); do
  curl -s -o /dev/null "${FRONTEND_URL}/products" || true
  if (( i % 5 == 0 )); then
    curl -s -o /dev/null "${FRONTEND_URL}/products/slow" || true
  fi
  if (( i % 9 == 0 )); then
    curl -s -o /dev/null "${FRONTEND_URL}/products/error" || true
  fi
  if (( i % 7 == 0 )); then
    curl -s -o /dev/null "${FRONTEND_URL}/ready" || true
  fi
  sleep 0.3
done

echo "Traffico completato. Aprire Prometheus su http://localhost:9090 e provare le query PromQL del laboratorio."

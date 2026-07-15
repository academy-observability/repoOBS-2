#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8118}"
ITERATIONS="${ITERATIONS:-20}"

echo "Genero traffico verso ${FRONTEND_URL}"

for i in $(seq 1 "$ITERATIONS"); do
  echo "Richiesta $i/$ITERATIONS"
  curl -sS "${FRONTEND_URL}/health" >/dev/null
  curl -sS "${FRONTEND_URL}/ready" >/dev/null || true
  curl -sS "${FRONTEND_URL}/products" >/dev/null || true
  if (( i % 5 == 0 )); then
    curl -sS "${FRONTEND_URL}/products/slow" >/dev/null || true
  fi
  if (( i % 7 == 0 )); then
    curl -sS "${FRONTEND_URL}/products/error" >/dev/null || true
  fi
  sleep 1
done

echo "Traffico completato. Aprire Prometheus, Grafana, Jaeger e i log container."

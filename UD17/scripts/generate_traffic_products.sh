#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${1:-}"
if [[ -z "$FRONTEND_URL" ]]; then
  echo "Uso: ./generate_traffic_products.sh https://<frontend-fqdn>"
  exit 1
fi
FRONTEND_URL="${FRONTEND_URL%/}"

NORMAL_COUNT="${NORMAL_COUNT:-20}"
SLEEP_SECONDS="${SLEEP_SECONDS:-2}"

echo "Genero traffico UD17 verso: $FRONTEND_URL"
echo "Normal count: $NORMAL_COUNT"

for i in $(seq 1 "$NORMAL_COUNT"); do
  TS="$(date +%s)"
  RID="ud17-products-${i}-${TS}"
  echo "[$i] request_id=$RID"

  curl -sS -H "X-Request-Id: $RID" "$FRONTEND_URL/products" >/dev/null

  curl -sS -H "X-Request-Id: $RID-slow" "$FRONTEND_URL/products/slow" >/dev/null || true

  if (( i % 5 == 0 )); then
    CODE=$(curl -sS -o /tmp/ud17-products-error.json -w "%{http_code}" -H "X-Request-Id: $RID-error" "$FRONTEND_URL/products/error" || true)
    echo "    products/error status=$CODE"
  fi

  sleep "$SLEEP_SECONDS"
done

echo "Traffico generato. Attendere alcuni minuti prima di interrogare Application Insights/Log Analytics."

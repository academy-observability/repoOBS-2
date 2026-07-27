#!/usr/bin/env bash
set -euo pipefail
SCENARIO="${1:-normal}"
BASE_URL="${2:-http://localhost:8118}"

case "$SCENARIO" in
  normal)
    PATHS=("/products" "/ready" "/version")
    ;;
  slow)
    PATHS=("/products/slow" "/products" "/products/slow")
    ;;
  error)
    PATHS=("/products/error" "/products" "/products/error")
    ;;
  mixed)
    PATHS=("/products" "/products/slow" "/products/error" "/ready")
    ;;
  *)
    echo "Scenario non valido: $SCENARIO" >&2
    echo "Uso: $0 normal|slow|error|mixed [BASE_URL]" >&2
    exit 1
    ;;
esac

echo "Scenario locale: $SCENARIO"
echo "Base URL: $BASE_URL"

for i in $(seq 1 20); do
  for p in "${PATHS[@]}"; do
    code_time=$(curl -s -o /dev/null -w "%{http_code} %{time_total}" "$BASE_URL$p" || echo "000 0")
    printf "%s iter=%02d path=%s result=%s\n" "$(date -Is)" "$i" "$p" "$code_time"
    sleep 0.3
  done
done

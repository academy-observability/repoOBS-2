#!/usr/bin/env bash
set -euo pipefail
SCENARIO="${1:-normal}"
BASE_URL="${2:-}"

if [[ -z "$BASE_URL" ]]; then
  echo "Uso: $0 normal|slow|error|mixed https://frontend-url" >&2
  exit 1
fi
BASE_URL="${BASE_URL%/}"

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
    exit 1
    ;;
esac

echo "Scenario cloud: $SCENARIO"
echo "Base URL: $BASE_URL"

for i in $(seq 1 20); do
  for p in "${PATHS[@]}"; do
    rid="ud24-$(date +%s)-$i"
    code_time=$(curl -s -o /dev/null -w "%{http_code} %{time_total}" -H "X-Request-Id: $rid" "$BASE_URL$p" || echo "000 0")
    printf "%s request_id=%s path=%s result=%s\n" "$(date -Is)" "$rid" "$p" "$code_time"
    sleep 0.5
  done
done

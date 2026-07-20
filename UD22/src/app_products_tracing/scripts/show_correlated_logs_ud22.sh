#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ $# -ne 1 ]]; then
  echo "Uso: ./scripts/show_correlated_logs_ud22.sh REQUEST_ID" >&2
  exit 1
fi

REQUEST_ID="$1"
echo "Log correlati per request_id=${REQUEST_ID}"
docker compose logs --no-color frontend-products backend-products \
  | grep -F "$REQUEST_ID" \
  || { echo "Nessuna riga trovata. Verificare l'identificatore e riprovare." >&2; exit 2; }

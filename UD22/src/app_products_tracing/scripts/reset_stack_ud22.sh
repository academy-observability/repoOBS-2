#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${RESET_UD22:-no}" != "yes" ]]; then
  cat <<'EOF'
Operazione annullata.
Questo reset elimina container, reti e i named volume della UD22, comprese le trace Jaeger.
Per confermare eseguire:
  RESET_UD22=yes ./scripts/reset_stack_ud22.sh
EOF
  exit 1
fi

echo "Eliminazione controllata dello stack e dei volumi UD22"
docker compose down -v --remove-orphans

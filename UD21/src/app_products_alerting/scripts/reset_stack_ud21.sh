#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${RESET_UD21:-no}" != "yes" ]]; then
  echo "Operazione annullata. Questo script elimina regole, contact point, metriche ed eventi salvati." >&2
  echo "Per confermare: RESET_UD21=yes ./scripts/reset_stack_ud21.sh" >&2
  exit 2
fi

echo "RESET DISTRUTTIVO UD21: rimozione container, reti e volumi..."
docker compose down -v --remove-orphans

echo "Reset completato. Il prossimo avvio ripartirà da zero."

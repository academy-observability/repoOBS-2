#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Arresto stack UD21 senza eliminare i volumi..."
docker compose down

echo "Volumi conservati:"
docker volume ls --filter name=obs-ud21 --format '  {{.Name}}'
echo "Per un reset distruttivo usare: RESET_UD21=yes ./scripts/reset_stack_ud21.sh"

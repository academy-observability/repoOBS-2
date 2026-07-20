#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p ../../logs
STAMP="$(date +%Y%m%d-%H%M%S)"
docker compose logs --no-color frontend-products > "../../logs/frontend-${STAMP}.log"
docker compose logs --no-color backend-products  > "../../logs/backend-${STAMP}.log"
echo "Log salvati nella cartella UD22/logs"

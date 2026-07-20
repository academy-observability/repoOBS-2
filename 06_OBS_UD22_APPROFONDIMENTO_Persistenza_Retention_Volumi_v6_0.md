#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "Arresto dei container UD22 senza eliminare dati o volumi"
docker compose stop

#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Arresto stack locale UD19"
docker compose down

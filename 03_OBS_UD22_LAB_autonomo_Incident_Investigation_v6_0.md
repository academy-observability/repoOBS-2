#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Ricreazione dei container; i named volume vengono conservati"
docker compose down --remove-orphans
docker compose up -d

for url in http://localhost:8022/health http://localhost:8122/health http://localhost:16686/; do
  for _ in $(seq 1 60); do
    curl -fsS "$url" >/dev/null 2>&1 && break
    sleep 2
  done
done

echo "Stack nuovamente disponibile. Le trace salvate in Badger devono essere ancora consultabili."

#!/usr/bin/env bash
set -euo pipefail

echo "Named volume della UD22"
docker volume inspect \
  obs-ud22-jaeger-data \
  obs-ud22-prometheus-data \
  obs-ud22-grafana-data \
  --format '{{.Name}}  mountpoint={{.Mountpoint}}' 2>/dev/null \
  || echo "Uno o più volumi non sono ancora stati creati. Avviare prima lo stack."

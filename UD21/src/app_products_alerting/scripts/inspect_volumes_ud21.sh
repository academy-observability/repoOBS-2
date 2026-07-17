#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

volumes=(
  obs-ud21-grafana-data
  obs-ud21-prometheus-data
  obs-ud21-webhook-data
)

echo "Volumi dichiarati dalla UD21:"
for volume in "${volumes[@]}"; do
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    mountpoint=$(docker volume inspect "$volume" --format '{{.Mountpoint}}')
    echo "  OK  $volume"
    echo "      Docker mountpoint: $mountpoint"
  else
    echo "  MISSING  $volume"
  fi
done

echo
echo "Mount presenti nei container:"
for container in ud21-grafana ud21-prometheus ud21-webhook-receiver; do
  if docker inspect "$container" >/dev/null 2>&1; then
    echo "[$container]"
    docker inspect "$container" --format '{{range .Mounts}}{{println "  " .Type .Name .Source "->" .Destination}}{{end}}'
  else
    echo "[$container] non avviato"
  fi
done

#!/usr/bin/env bash
set -euo pipefail
OUT_DIR="${1:-UD24/logs}"
mkdir -p "$OUT_DIR"

docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Networks}}\t{{.Ports}}" > "$OUT_DIR/docker_ps.txt" || true
docker network ls > "$OUT_DIR/docker_network_ls.txt" || true
docker logs frontend-products > "$OUT_DIR/frontend-products.log" 2>&1 || true
docker logs backend-products > "$OUT_DIR/backend-products.log" 2>&1 || true

echo "Evidenze locali salvate in $OUT_DIR"

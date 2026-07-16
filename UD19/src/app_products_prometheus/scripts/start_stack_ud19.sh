#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Avvio stack locale UD19: app-stack + obs-stack"
docker compose up -d --build

echo
echo "Container avviati:"
docker compose ps

echo
echo "URL principali:"
echo "Frontend Catalogo prodotti: http://localhost:8118/"
echo "Backend health:            http://localhost:8018/health"
echo "Prometheus:                http://localhost:9090"
echo "Grafana:                   http://localhost:3000  admin/admin"
echo "Jaeger:                    http://localhost:16686"

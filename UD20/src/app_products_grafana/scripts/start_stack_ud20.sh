#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Avvio stack locale UD20: app-stack products + obs-stack con dashboard Grafana"
docker compose up -d --build

echo
echo "Container avviati:"
docker compose ps

echo
echo "URL principali:"
echo "Frontend Catalogo prodotti: http://localhost:8120/"
echo "Backend health:            http://localhost:8020/health"
echo "Prometheus:                http://localhost:9090"
echo "Grafana:                   http://localhost:3000  admin/admin"
echo "Jaeger:                    http://localhost:16686"
echo
echo "Dopo qualche secondo aprire Grafana e cercare la dashboard:"
echo "Academy Observability / UD20 - Catalogo prodotti - FE/BE metrics"

#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

wait_url() {
  local name="$1"
  local url="$2"
  local attempts="${3:-60}"
  for _ in $(seq 1 "$attempts"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      printf "[OK] %s\n" "$name"
      return 0
    fi
    sleep 2
  done
  printf "[ERRORE] %s non disponibile: %s\n" "$name" "$url" >&2
  return 1
}

echo "Avvio stack UD22"
docker compose up -d --build

echo
echo "Attesa dei servizi..."
wait_url "Backend" "http://localhost:8022/health"
wait_url "Frontend" "http://localhost:8122/health"
wait_url "Prometheus" "http://localhost:9090/-/ready"
wait_url "Grafana" "http://localhost:3000/api/health"
wait_url "Jaeger" "http://localhost:16686/"

echo
docker compose ps

echo
echo "URL principali"
echo "Frontend:   http://localhost:8122"
echo "Backend:    http://localhost:8022/health"
echo "Prometheus: http://localhost:9090"
echo "Grafana:    http://localhost:3000  admin/admin"
echo "Jaeger:     http://localhost:16686"
echo
echo "Volumi persistenti montati:"
echo "  obs-ud22-jaeger-data     -> /badger"
echo "  obs-ud22-prometheus-data -> /prometheus"
echo "  obs-ud22-grafana-data     -> /var/lib/grafana"

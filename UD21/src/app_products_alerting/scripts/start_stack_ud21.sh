#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1; then
  echo "ERRORE: Docker non è disponibile nel PATH." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "ERRORE: Docker Compose plugin non è disponibile." >&2
  exit 1
fi

echo "Avvio stack UD21 con volumi persistenti..."
docker compose up -d --build

wait_url() {
  local name="$1"
  local url="$2"
  local attempts="${3:-60}"
  for _ in $(seq 1 "$attempts"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "OK  ${name}: ${url}"
      return 0
    fi
    sleep 2
  done
  echo "ERRORE: ${name} non è pronto: ${url}" >&2
  return 1
}

echo
echo "Attesa servizi..."
wait_url "Frontend" "http://localhost:8121/health"
wait_url "Prometheus" "http://localhost:9090/-/ready"
wait_url "Grafana" "http://localhost:3000/api/health"
wait_url "Webhook receiver" "http://localhost:5001/health"
wait_url "Jaeger" "http://localhost:16686"

echo
echo "Container:"
docker compose ps

echo
echo "Volumi persistenti UD21:"
docker volume ls --filter name=obs-ud21 --format '  {{.Name}}'

echo
echo "URL principali:"
echo "  Frontend:          http://localhost:8121/"
echo "  Backend health:    http://localhost:8021/health"
echo "  Prometheus:        http://localhost:9090"
echo "  Grafana:           http://localhost:3000  admin/admin"
echo "  Webhook events:    http://localhost:5001/events"
echo "  Jaeger:            http://localhost:16686"
echo
echo "NOTA: stop_stack_ud21.sh conserva i volumi."
echo "      reset_stack_ud21.sh li elimina solo con RESET_UD21=yes."

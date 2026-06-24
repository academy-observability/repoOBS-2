#!/usr/bin/env bash
set -euo pipefail

PORT="9199"
LOG_FILE="logs/verification_app.log"
REPORT_FILE="evidence/verification_sli_report.json"

mkdir -p logs evidence
: > "$LOG_FILE"

python3 -m py_compile src/observable_service.py src/parse_sli.py

PORT="$PORT" LOG_PATH="$LOG_FILE" python3 src/observable_service.py > logs/verification_service.out 2>&1 &
PID=$!
trap 'kill "$PID" 2>/dev/null || true' EXIT

READY_OK=0
for _ in $(seq 1 20); do
  if curl -fsS "http://localhost:${PORT}/health" > /dev/null 2>&1; then
    READY_OK=1
    break
  fi
  sleep 0.25
done

if [[ "$READY_OK" != "1" ]]; then
  echo "Service did not become ready on port $PORT"
  cat logs/verification_service.out || true
  exit 1
fi

curl -fsS "http://localhost:${PORT}/ready" > /dev/null
curl -fsS "http://localhost:${PORT}/metrics" > /dev/null
curl -fsS -H 'X-Request-Id: verifica-ud04-001' "http://localhost:${PORT}/work?ms=80" > /dev/null
curl -s "http://localhost:${PORT}/fail" > /dev/null || true
curl -s "http://localhost:${PORT}/missing" > /dev/null || true

python3 src/parse_sli.py "$LOG_FILE" "$REPORT_FILE" > /dev/null

grep 'verifica-ud04-001' "$LOG_FILE" > /dev/null
test -s "$REPORT_FILE"
python3 -m json.tool "$REPORT_FILE" > /dev/null

echo "UD04 verification completed"
echo "Log: $LOG_FILE"
echo "Report: $REPORT_FILE"

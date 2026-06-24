#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-9100}"
N="${2:-30}"
BASE="http://localhost:${PORT}"
OUT="logs/traffic_responses.txt"

mkdir -p logs
: > "$OUT"

echo "Generating traffic against $BASE" | tee -a "$OUT"

for i in $(seq 1 "$N"); do
  curl -s -i -H "X-Request-Id: traffic-${i}-health" "$BASE/health" >> "$OUT"
  echo "" >> "$OUT"

  curl -s -i -H "X-Request-Id: traffic-${i}-work" "$BASE/work?ms=$(( (i % 5) * 80 ))" >> "$OUT"
  echo "" >> "$OUT"

  if (( i % 4 == 0 )); then
    curl -s -i -H "X-Request-Id: traffic-${i}-missing" "$BASE/nope" >> "$OUT"
    echo "" >> "$OUT"
  fi

  if (( i % 5 == 0 )); then
    curl -s -i -H "X-Request-Id: traffic-${i}-fail" "$BASE/fail" >> "$OUT"
    echo "" >> "$OUT"
  fi

  if (( i % 6 == 0 )); then
    curl -s -i -X POST -H "X-Request-Id: traffic-${i}-badjson" -H 'Content-Type: application/json' -d '{"msg":' "$BASE/echo" >> "$OUT" || true
    echo "" >> "$OUT"
  else
    curl -s -i -X POST -H "X-Request-Id: traffic-${i}-echo" -H 'Content-Type: application/json' -d '{"msg":"ciao"}' "$BASE/echo" >> "$OUT"
    echo "" >> "$OUT"
  fi

done

echo "DONE. Responses saved to $OUT" | tee -a "$OUT"

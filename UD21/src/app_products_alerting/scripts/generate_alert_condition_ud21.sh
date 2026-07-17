#!/usr/bin/env bash
set -euo pipefail

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8121}"
DURATION_SECONDS="${DURATION_SECONDS:-180}"
SLEEP_SECONDS="${SLEEP_SECONDS:-0.15}"

end=$((SECONDS + DURATION_SECONDS))
echo "Genero error burst UD21 per circa ${DURATION_SECONDS}s"
echo "Rapporto richieste: una normale e una in errore, quindi error rate atteso vicino al 50%."

while (( SECONDS < end )); do
  curl -s -o /dev/null "${FRONTEND_URL}/products" || true
  curl -s -o /dev/null "${FRONTEND_URL}/products/error" || true
  sleep "$SLEEP_SECONDS"
done

echo "Error burst terminato. Attendere il decadimento della finestra [2m] per il resolved."

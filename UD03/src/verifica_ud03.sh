#!/usr/bin/env bash
set -euo pipefail

EVIDENCE="docs/evidence_ud03.md"
ERRORS=0

check_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    echo "[OK] File presente: $file"
  else
    echo "[ERRORE] File mancante: $file"
    ERRORS=$((ERRORS+1))
  fi
}

check_dir() {
  local dir="$1"
  if [[ -d "$dir" ]]; then
    echo "[OK] Directory presente: $dir"
  else
    echo "[ERRORE] Directory mancante: $dir"
    ERRORS=$((ERRORS+1))
  fi
}

check_contains() {
  local file="$1"
  local pattern="$2"
  if [[ -f "$file" ]] && grep -qi "$pattern" "$file"; then
    echo "[OK] Evidenza contiene: $pattern"
  else
    echo "[AVVISO] Evidenza non contiene ancora: $pattern"
  fi
}

echo "== Verifica OBS_UD03 =="

check_dir "src"
check_dir "docs"
check_dir "logs"
check_file "src/http_lab_server.py"
check_file "src/net_snapshot.sh"
check_file "$EVIDENCE"

check_contains "$EVIDENCE" "DNS"
check_contains "$EVIDENCE" "HTTP"
check_contains "$EVIDENCE" "porta"
check_contains "$EVIDENCE" "404"
check_contains "$EVIDENCE" "500"
check_contains "$EVIDENCE" "Sintomo"
check_contains "$EVIDENCE" "Ipotesi"
check_contains "$EVIDENCE" "Interpretazione"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo
  echo "== Stato Git sintetico =="
  git status --short
else
  echo "[INFO] Questa cartella non sembra essere dentro un repository Git."
fi

echo
if [[ "$ERRORS" -eq 0 ]]; then
  echo "Verifica completata: struttura minima presente."
else
  echo "Verifica completata con $ERRORS errore/i strutturali."
  exit 1
fi

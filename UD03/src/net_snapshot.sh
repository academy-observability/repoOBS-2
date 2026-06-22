#!/usr/bin/env bash
set -euo pipefail

OUT="logs/net_snapshot_ud03.txt"
mkdir -p logs

{
  echo "# OBS_UD03 - Snapshot rete"
  date
  echo
  echo "## Hostname"
  hostname || true
  echo
  echo "## Interfacce - ip a"
  ip a || true
  echo
  echo "## Routing - ip r"
  ip r || true
  echo
  echo "## DNS - /etc/resolv.conf"
  cat /etc/resolv.conf || true
  echo
  echo "## Porte TCP in ascolto - ss -ltnp"
  ss -ltnp || true
  echo
  echo "## Strumenti disponibili"
  for cmd in ip ping curl ss python3 dig nslookup traceroute tracepath nc; do
    printf '%-12s' "$cmd"
    command -v "$cmd" || true
  done
} > "$OUT"

echo "Snapshot creato: $OUT"
wc -l "$OUT"

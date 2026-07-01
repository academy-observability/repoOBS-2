#!/usr/bin/env bash
set -euo pipefail

# UD07 - Verifica ambiente
# Eseguire dal repository locale, non da Cloud Shell, se si vogliono produrre file in evidence/.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/ud07.env"

cd "$ROOT_DIR"
mkdir -p evidence logs docs img

if [[ -f "$CONFIG_FILE" ]]; then
  # Carica variabili non segrete del laboratorio.
  set -a
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
  set +a
fi

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"
}

log "Verifica UD07"

if ! command -v az >/dev/null 2>&1; then
  echo "ERRORE: Azure CLI non trovato." >&2
  exit 1
fi

log "Azure CLI disponibile: $(az version --query '"azure-cli"' -o tsv 2>/dev/null || echo 'versione non rilevata')"

if ! az account show >/dev/null 2>&1; then
  echo "ERRORE: nessun login Azure attivo. Eseguire: az login --use-device-code" >&2
  exit 1
fi

if [[ -n "${SUB_ID:-}" && "$SUB_ID" != "<id-subscription>" ]]; then
  log "Imposto subscription da config: $SUB_ID"
  az account set --subscription "$SUB_ID"
fi

az account show -o json > evidence/ud07_account_context.json
az account show --query "{subscription:name,id:id,user:user.name}" --output table

if [[ -n "${RG_NAME:-}" && "$RG_NAME" != "rg-obs-ud05-<codice>" ]]; then
  log "Verifico Resource Group: $RG_NAME"
  az group exists --name "$RG_NAME" | tee evidence/ud07_rg_exists.txt
fi

if command -v jq >/dev/null 2>&1; then
  log "jq disponibile."
else
  log "jq non disponibile. Per leggere JSON usare: python3 -m json.tool <file>"
fi

log "File creato: evidence/ud07_account_context.json"
log "Verifica completata."

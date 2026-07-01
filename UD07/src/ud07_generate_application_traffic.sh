#!/usr/bin/env bash
set -u
set -o pipefail

# UD07 - Generazione traffico applicativo/workload controllato
# Scopo:
#   Generare segnali osservabili su App Service, Storage Account e VM opzionale.
# Ambiente:
#   Eseguire da WSL o terminale locale dentro la cartella UD07.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/ud07.env"

cd "$ROOT_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
  set +a
fi

SUB_ID="${SUB_ID:-}"
RG_NAME="${RG_NAME:-}"
STORAGE_NAME="${STORAGE_NAME:-}"
APP_NAME="${APP_NAME:-}"
VM_NAME="${VM_NAME:-}"

APP_REQUESTS="${APP_REQUESTS:-40}"
APP_404_REQUESTS="${APP_404_REQUESTS:-10}"
STORAGE_OPS="${STORAGE_OPS:-20}"
WAIT_METRICS_SECONDS="${WAIT_METRICS_SECONDS:-180}"
RUN_VM_PROBE="${RUN_VM_PROBE:-0}"
VM_CPU_SECONDS="${VM_CPU_SECONDS:-20}"
COMPUTE_API_VERSION="${COMPUTE_API_VERSION:-2025-04-01}"

mkdir -p logs evidence tmp

MAIN_LOG="logs/ud07_application_traffic.log"
ERROR_LOG="logs/ud07_application_traffic_errors.log"
APP_CSV="logs/ud07_appservice_http_traffic.csv"
STORAGE_CSV="logs/ud07_storage_blob_traffic.csv"

: > "$MAIN_LOG"
: > "$ERROR_LOG"
printf "timestamp,kind,url,http_status,time_total_seconds\n" > "$APP_CSV"
printf "timestamp,operation,blob_name,result\n" > "$STORAGE_CSV"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$MAIN_LOG"
}

warn() {
  printf '[%s] WARNING: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$ERROR_LOG" >&2
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Comando mancante: $1" >&2
    exit 1
  fi
}

invalid_value() {
  local value="$1"
  [[ -z "$value" || "$value" == *"<"* ]]
}

require_command az
require_command curl

if invalid_value "$SUB_ID" || invalid_value "$RG_NAME"; then
  warn "SUB_ID o RG_NAME non configurati. Controlla config/ud07.env."
  exit 1
fi

log "Imposto subscription: $SUB_ID"
az account set --subscription "$SUB_ID" 2>>"$ERROR_LOG" || {
  warn "Impossibile impostare la subscription."
  exit 1
}

log "Contesto Azure attivo"
az account show --query "{subscription:name,id:id,user:user.name}" --output table | tee -a "$MAIN_LOG"

log "Recupero Resource ID e hostname delle risorse principali"

APP_HOST=""
APP_ID=""
STORAGE_ID=""
VM_ID=""

if ! invalid_value "$APP_NAME"; then
  APP_HOST="$(az webapp show --name "$APP_NAME" --resource-group "$RG_NAME" --query defaultHostName --output tsv 2>>"$ERROR_LOG" || true)"
  APP_ID="$(az webapp show --name "$APP_NAME" --resource-group "$RG_NAME" --query id --output tsv 2>>"$ERROR_LOG" || true)"
fi

if ! invalid_value "$STORAGE_NAME"; then
  STORAGE_ID="$(az storage account show --name "$STORAGE_NAME" --resource-group "$RG_NAME" --query id --output tsv 2>>"$ERROR_LOG" || true)"
fi

if ! invalid_value "$VM_NAME"; then
  VM_ID="$(az vm show --name "$VM_NAME" --resource-group "$RG_NAME" --query id --output tsv 2>>"$ERROR_LOG" || true)"
fi

printf "APP_HOST=%s\nAPP_ID=%s\nSTORAGE_ID=%s\nVM_ID=%s\n" \
  "$APP_HOST" "$APP_ID" "$STORAGE_ID" "$VM_ID" | tee evidence/ud07_application_traffic_resource_ids.txt

# 1. Traffico HTTP App Service.
if [[ -n "$APP_HOST" ]]; then
  log "Genero $APP_REQUESTS richieste HTTP verso App Service: https://$APP_HOST/"

  for i in $(seq 1 "$APP_REQUESTS"); do
    URL="https://$APP_HOST/"
    RESULT="$(curl -sS -o /dev/null -w "%{http_code},%{time_total}" --max-time 10 "$URL" 2>>"$ERROR_LOG" || printf "000,0")"
    printf "%s,home,%s,%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$URL" "$RESULT" >> "$APP_CSV"
    sleep 1
  done

  log "Genero $APP_404_REQUESTS richieste su URL inesistenti per eventuali 404."

  for i in $(seq 1 "$APP_404_REQUESTS"); do
    URL="https://$APP_HOST/ud07-not-found-$i"
    RESULT="$(curl -sS -o /dev/null -w "%{http_code},%{time_total}" --max-time 10 "$URL" 2>>"$ERROR_LOG" || printf "000,0")"
    printf "%s,not_found,%s,%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$URL" "$RESULT" >> "$APP_CSV"
    sleep 1
  done
else
  warn "APP_HOST vuoto: salto traffico HTTP App Service."
fi

# 2. Traffico Storage Blob.
if [[ -n "$STORAGE_ID" ]]; then
  log "Genero traffico Blob Storage."

  STORAGE_KEY="$(az storage account keys list --account-name "$STORAGE_NAME" --resource-group "$RG_NAME" --query "[0].value" --output tsv 2>>"$ERROR_LOG" || true)"
  CONTAINER_NAME="ud07-app-traffic"

  if [[ -n "$STORAGE_KEY" ]]; then
    az storage container create \
      --account-name "$STORAGE_NAME" \
      --account-key "$STORAGE_KEY" \
      --name "$CONTAINER_NAME" \
      --output none 2>>"$ERROR_LOG" \
      || warn "Creazione container fallita o container non gestibile."

    for i in $(seq 1 "$STORAGE_OPS"); do
      LOCAL_FILE="tmp/ud07_blob_${i}.txt"
      DOWNLOADED_FILE="tmp/ud07_blob_${i}_downloaded.txt"
      BLOB_NAME="ud07/blob-${i}.txt"

      printf "UD07 storage workload probe %s - %s\n" "$i" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$LOCAL_FILE"

      if az storage blob upload --account-name "$STORAGE_NAME" --account-key "$STORAGE_KEY" --container-name "$CONTAINER_NAME" --name "$BLOB_NAME" --file "$LOCAL_FILE" --overwrite true --output none 2>>"$ERROR_LOG"; then
        printf "%s,upload,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> "$STORAGE_CSV"
      else
        printf "%s,upload,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> "$STORAGE_CSV"
      fi

      az storage blob list --account-name "$STORAGE_NAME" --account-key "$STORAGE_KEY" --container-name "$CONTAINER_NAME" --prefix "ud07/" --output none 2>>"$ERROR_LOG" \
        && printf "%s,list,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "ud07/" >> "$STORAGE_CSV" \
        || printf "%s,list,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "ud07/" >> "$STORAGE_CSV"

      az storage blob download --account-name "$STORAGE_NAME" --account-key "$STORAGE_KEY" --container-name "$CONTAINER_NAME" --name "$BLOB_NAME" --file "$DOWNLOADED_FILE" --overwrite true --output none 2>>"$ERROR_LOG" \
        && printf "%s,download,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> "$STORAGE_CSV" \
        || printf "%s,download,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> "$STORAGE_CSV"

      az storage blob delete --account-name "$STORAGE_NAME" --account-key "$STORAGE_KEY" --container-name "$CONTAINER_NAME" --name "$BLOB_NAME" --output none 2>>"$ERROR_LOG" \
        && printf "%s,delete,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> "$STORAGE_CSV" \
        || printf "%s,delete,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> "$STORAGE_CSV"

      sleep 1
    done
  else
    warn "STORAGE_KEY vuota: salto traffico Storage. Possibili permessi insufficienti."
  fi
else
  warn "STORAGE_ID vuoto: salto traffico Storage."
fi

# 3. VM workload opzionale.
if [[ "$RUN_VM_PROBE" == "1" && -n "$VM_ID" ]]; then
  log "Verifico stato VM tramite Azure Resource Manager REST."

  VM_POWER_STATE="$(az rest --method get --url "https://management.azure.com${VM_ID}/instanceView?api-version=${COMPUTE_API_VERSION}" --query "statuses[?starts_with(code, 'PowerState/')].code | [0]" --output tsv 2>>"$ERROR_LOG" || true)"
  log "Stato VM rilevato: ${VM_POWER_STATE:-non disponibile}"

  if [[ "$VM_POWER_STATE" == "PowerState/running" ]]; then
    log "Genero piccolo carico CPU nella VM con RunCommand per $VM_CPU_SECONDS secondi."

    az vm run-command invoke \
      --resource-group "$RG_NAME" \
      --name "$VM_NAME" \
      --command-id RunShellScript \
      --scripts "echo 'UD07 workload probe - ' \$(date -u) | sudo tee -a /var/log/ud07-workload-probe.log; timeout ${VM_CPU_SECONDS}s bash -c 'while true; do :; done'" \
      --output json > evidence/ud07_vm_workload_runcommand.json 2>>"$ERROR_LOG" \
      || warn "RunCommand VM non riuscito."
  else
    warn "VM non running o stato non disponibile: salto probe CPU VM."
  fi
else
  log "Probe VM disabilitato o VM_ID vuoto. RUN_VM_PROBE=$RUN_VM_PROBE"
fi

# 4. Attesa e raccolta metriche.
log "Attendo $WAIT_METRICS_SECONDS secondi per propagazione metriche Azure Monitor."
sleep "$WAIT_METRICS_SECONDS"

if [[ -n "$APP_ID" ]]; then
  log "Salvo metrica App Service Requests."
  az monitor metrics list --resource "$APP_ID" --metric "Requests" --interval PT1M --aggregation Total --output json > evidence/ud07_appservice_requests_after_application_traffic.json 2>>"$ERROR_LOG" \
    || warn "Raccolta metrica Requests fallita."
fi

if [[ -n "$STORAGE_ID" ]]; then
  log "Salvo metrica Storage Transactions."
  az monitor metrics list --resource "$STORAGE_ID" --metric "Transactions" --interval PT1M --aggregation Total --output json > evidence/ud07_storage_transactions_after_application_traffic.json 2>>"$ERROR_LOG" \
    || warn "Raccolta metrica Transactions fallita."
fi

if [[ -n "$VM_ID" ]]; then
  log "Salvo metrica VM Percentage CPU."
  az monitor metrics list --resource "$VM_ID" --metric "Percentage CPU" --interval PT1M --aggregation Average Maximum --output json > evidence/ud07_vm_cpu_after_workload_probe.json 2>>"$ERROR_LOG" \
    || warn "Raccolta metrica Percentage CPU fallita."
fi

cat <<MSG | tee -a "$MAIN_LOG"

============================================================
Cosa vedere dal Portale Azure
============================================================
1. App Service -> Metrics -> Requests -> Total.
2. Storage Account -> Metrics -> Transactions -> Total.
3. VM -> Metrics -> Percentage CPU -> Average / Maximum, se VM usata.

Nota didattica:
Questo script genera workload o traffico, quindi i segnali attesi sono metriche operative.
Non confonderlo con lo script amministrativo, che genera Activity Log.
============================================================
MSG

log "File prodotti:"
find logs evidence -maxdepth 1 -type f | sort | tee -a "$MAIN_LOG"
log "Fine script traffico applicativo UD07."

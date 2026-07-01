#!/usr/bin/env bash
set -u
set -o pipefail

# UD07 - Generazione attività amministrativa controllata
# Scopo:
#   Generare eventi nel piano di controllo Azure aggiornando tag su risorse core.
#   Produce Activity Log e modifica tag. Non genera traffico applicativo.
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

ADMIN_ROUNDS="${ADMIN_ROUNDS:-${ROUNDS:-3}}"
SLEEP_BETWEEN_RESOURCES="${SLEEP_BETWEEN_RESOURCES:-3}"
SLEEP_BETWEEN_ROUNDS="${SLEEP_BETWEEN_ROUNDS:-10}"
WAIT_ACTIVITY_LOG_SECONDS="${WAIT_ACTIVITY_LOG_SECONDS:-60}"

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p logs evidence

LOG_FILE="logs/ud07_admin_activity.log"
ERR_FILE="logs/ud07_admin_errors.log"
RESOURCE_IDS_FILE="logs/ud07_admin_resource_ids_core.txt"

: > "$LOG_FILE"
: > "$ERR_FILE"
: > "$RESOURCE_IDS_FILE"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$LOG_FILE"
}

err() {
  printf '[%s] ERRORE: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$ERR_FILE" >&2
}

require_value() {
  local name="$1"
  local value="$2"
  if [[ -z "$value" || "$value" == *"<"* ]]; then
    err "Variabile non configurata: $name. Controlla config/ud07.env."
    exit 1
  fi
}

get_id_or_empty() {
  local label="$1"
  shift
  local value
  value="$($@ 2>>"$ERR_FILE" || true)"
  if [[ -z "$value" ]]; then
    err "Resource ID non recuperato per: $label. La risorsa sarà saltata."
  else
    log "$label: $value"
    printf '%s\n' "$value" >> "$RESOURCE_IDS_FILE"
  fi
}

main() {
  log "Inizio generazione attività amministrativa UD07."

  if ! command -v az >/dev/null 2>&1; then
    err "Azure CLI non trovato."
    exit 1
  fi

  require_value "SUB_ID" "$SUB_ID"
  require_value "RG_NAME" "$RG_NAME"

  log "Imposto subscription: $SUB_ID"
  if ! az account set --subscription "$SUB_ID" 2>>"$ERR_FILE"; then
    err "Impossibile impostare la subscription. Verifica login e permessi."
    exit 1
  fi

  az account show --query "{subscription:name,id:id,user:user.name}" --output table | tee -a "$LOG_FILE"

  log "Recupero Resource ID delle risorse core. L'App Service Plan è escluso di proposito."

  if [[ -n "$STORAGE_NAME" && "$STORAGE_NAME" != *"<"* ]]; then
    get_id_or_empty "Storage Account" az storage account show --name "$STORAGE_NAME" --resource-group "$RG_NAME" --query id --output tsv
  fi

  if [[ -n "$APP_NAME" && "$APP_NAME" != *"<"* ]]; then
    get_id_or_empty "App Service" az webapp show --name "$APP_NAME" --resource-group "$RG_NAME" --query id --output tsv
  fi

  if [[ -n "$VM_NAME" && "$VM_NAME" != *"<"* ]]; then
    get_id_or_empty "Virtual Machine" az vm show --name "$VM_NAME" --resource-group "$RG_NAME" --query id --output tsv
  fi

  if [[ ! -s "$RESOURCE_IDS_FILE" ]]; then
    err "Nessuna risorsa core recuperata. Controlla config/ud07.env."
    exit 1
  fi

  log "Risorse che saranno aggiornate:"
  cat "$RESOURCE_IDS_FILE" | tee -a "$LOG_FILE"

  local failures=0

  for round in $(seq 1 "$ADMIN_ROUNDS"); do
    log "=== Round amministrativo $round/$ADMIN_ROUNDS ==="

    while read -r RESOURCE_ID; do
      [[ -z "$RESOURCE_ID" ]] && continue
      log "Aggiorno tag su: $RESOURCE_ID"

      if az tag update \
        --resource-id "$RESOURCE_ID" \
        --operation Merge \
        --tags \
          "ud07AdminProbe=round-${round}" \
          "ud07AdminRunId=${RUN_ID}" \
          "ud07LastAdminProbe=$(date -u +%Y%m%dT%H%M%SZ)" \
        --output none 2>>"$ERR_FILE"; then
        log "OK aggiornamento tag."
      else
        err "Aggiornamento tag fallito su: $RESOURCE_ID"
        failures=$((failures + 1))
      fi

      sleep "$SLEEP_BETWEEN_RESOURCES"
    done < "$RESOURCE_IDS_FILE"

    sleep "$SLEEP_BETWEEN_ROUNDS"
  done

  if [[ "$failures" -gt 0 ]]; then
    err "Completato con $failures errori. Vedi $ERR_FILE."
  else
    log "Completato senza errori di aggiornamento tag."
  fi

  log "Attendo $WAIT_ACTIVITY_LOG_SECONDS secondi per propagazione Activity Log."
  sleep "$WAIT_ACTIVITY_LOG_SECONDS"

  log "Salvo Activity Log del Resource Group in JSON."
  az monitor activity-log list \
    --resource-group "$RG_NAME" \
    --max-events 80 \
    --output json > evidence/ud07_admin_activity_log_after_core_tag_updates.json 2>>"$ERR_FILE" \
    || err "Raccolta Activity Log JSON fallita."

  log "Salvo Activity Log del Resource Group in tabella."
  az monitor activity-log list \
    --resource-group "$RG_NAME" \
    --max-events 30 \
    --query "[].{Time:eventTimestamp,Operation:operationName.localizedValue,Status:status.localizedValue,Caller:caller,Resource:resourceId}" \
    --output table > evidence/ud07_admin_activity_log_after_core_tag_updates_table.txt 2>>"$ERR_FILE" \
    || err "Raccolta Activity Log tabellare fallita."

  log "Salvo tag finali delle risorse core recuperate."
  az resource list \
    --resource-group "$RG_NAME" \
    --query "[?name=='$STORAGE_NAME' || name=='$APP_NAME' || name=='$VM_NAME'].{Name:name,Type:type,Tags:tags}" \
    --output json > evidence/ud07_admin_resource_tags_after_updates.json 2>>"$ERR_FILE" \
    || err "Raccolta tag finali fallita."

  cat <<MSG | tee -a "$LOG_FILE"

============================================================
Cosa vedere dal Portale Azure
============================================================
1. Resource groups -> $RG_NAME -> Activity log -> Last hour.
2. Aprire le risorse core e controllare Activity log e Tags.
3. Tag attesi:
   - ud07AdminProbe
   - ud07AdminRunId
   - ud07LastAdminProbe

Nota didattica:
Questo script genera segnali amministrativi del piano di controllo Azure.
Non genera traffico applicativo.
============================================================
MSG

  log "File prodotti:"
  find logs evidence -maxdepth 1 -type f | sort | tee -a "$LOG_FILE"
  log "Fine script amministrativo UD07."
}

main "$@"

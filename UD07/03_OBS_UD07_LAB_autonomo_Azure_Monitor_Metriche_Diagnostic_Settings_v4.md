# 03 - Laboratorio autonomo UD07 v4

# Report metriche, segnali generati e Diagnostic Settings

## 1. Obiettivo

Nel laboratorio autonomo applichiamo il metodo della mattina a una risorsa scelta o assegnata.

Non bisogna ripetere tutto il guidato. Bisogna scegliere uno scenario, generare un segnale controllato e interpretarlo.

Formula del lavoro:

```text
risorsa → domanda diagnostica → baseline → attività controllata → osservazione dopo → evidenza → interpretazione
```

## 2. Regole operative

```text
Non creare nuove risorse Azure.
Non eliminare risorse.
Non configurare Diagnostic Settings reali senza autorizzazione.
Eseguire i comandi che scrivono file dal repository locale, non da Cloud Shell.
Usare Cloud Shell solo per controlli rapidi o output da copiare.
```

## 3. Preparazione

Entrare nella cartella UD07:

```bash
cd ~/corso_obs/obs-labs-2026-*/work/UD07
```

Preparare cartelle:

```bash
mkdir -p docs evidence logs img
```

Caricare configurazione:

```bash
set -a
source config/ud07.env
set +a
```

Verificare contesto:

```bash
./src/verifica_ud07.sh
```

## 4. Scegliere uno scenario

Scegliere uno scenario tra i seguenti.

| Scenario | Risorsa | Domanda diagnostica |
|---|---|---|
| A | App Service | l'app riceve richieste dopo traffico controllato? |
| B | Storage Account | lo storage produce transazioni dopo operazioni blob? |
| C | VM | la VM mostra carico CPU dopo workload controllato? |
| D | Risorsa core | Activity Log registra modifiche amministrative? |

Non scegliere tutto. Scegliere bene. Il “faccio tutto” è spesso il modo più costoso per non capire niente.

## 5. Creare il report autonomo

```bash
cp docs/template_report_ud07_autonomo.md docs/report_ud07_autonomo.md
```

Compilare subito le prime sezioni:

```text
Risorsa scelta
Domanda diagnostica
Segnale atteso
```

## 6. Scenario A: App Service Requests

### Baseline dal Portale

```text
App Service
→ Metrics
→ Requests
→ Aggregation: Total
→ Time range: Last hour
```

Salvare screenshot:

```text
img/ud07_autonomo_appservice_baseline.png
```

### Baseline da CLI

```bash
APP_ID="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"

bash src/az_metrics_snapshot.sh "$APP_ID" "Requests" PT1M Total evidence/ud07_autonomo_appservice_requests_baseline.json
```

### Generare traffico

È possibile usare lo script completo oppure una sequenza breve.

Sequenza breve:

```bash
APP_HOST="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query defaultHostName \
  --output tsv)"

for i in $(seq 1 40)
do
  curl -s -o /dev/null \
    -w "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ) status=%{http_code} time=%{time_total}\n" \
    "https://$APP_HOST/" | tee -a logs/ud07_autonomo_appservice_curl.log
  sleep 1
done
```

### Dopo il traffico

Attendere:

```bash
sleep 180
```

Salvare evidenza:

```bash
bash src/az_metrics_snapshot.sh "$APP_ID" "Requests" PT1M Total evidence/ud07_autonomo_appservice_requests_after.json
```

Screenshot:

```text
img/ud07_autonomo_appservice_after.png
```

## 7. Scenario B: Storage Transactions

### Baseline dal Portale

```text
Storage Account
→ Metrics
→ Transactions
→ Aggregation: Total
→ Time range: Last hour
```

Screenshot:

```text
img/ud07_autonomo_storage_baseline.png
```

### Baseline da CLI

```bash
STORAGE_ID="$(az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"

bash src/az_metrics_snapshot.sh "$STORAGE_ID" "Transactions" PT1M Total evidence/ud07_autonomo_storage_transactions_baseline.json
```

### Generare operazioni blob

```bash
STORAGE_KEY="$(az storage account keys list \
  --account-name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query "[0].value" \
  --output tsv)"

CONTAINER_NAME="ud07-autonomo"

az storage container create \
  --account-name "$STORAGE_NAME" \
  --account-key "$STORAGE_KEY" \
  --name "$CONTAINER_NAME" \
  --output none

for i in $(seq 1 20)
do
  FILE="logs/ud07_autonomo_blob_${i}.txt"
  BLOB="autonomo/blob-${i}.txt"
  echo "UD07 autonomo storage $i $(date -u)" > "$FILE"

  az storage blob upload \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --container-name "$CONTAINER_NAME" \
    --name "$BLOB" \
    --file "$FILE" \
    --overwrite true \
    --output none

  az storage blob list \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --container-name "$CONTAINER_NAME" \
    --prefix "autonomo/" \
    --output none

  sleep 1
done
```

### Dopo le operazioni

```bash
sleep 180

bash src/az_metrics_snapshot.sh "$STORAGE_ID" "Transactions" PT1M Total evidence/ud07_autonomo_storage_transactions_after.json
```

Screenshot:

```text
img/ud07_autonomo_storage_after.png
```

## 8. Scenario C: VM Percentage CPU

Usare solo se la VM è running e il docente autorizza RunCommand.

```bash
VM_ID="$(az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

Baseline:

```bash
bash src/az_metrics_snapshot.sh "$VM_ID" "Percentage CPU" PT1M "Average Maximum" evidence/ud07_autonomo_vm_cpu_baseline.json
```

Verificare stato:

```bash
az rest \
  --method get \
  --url "https://management.azure.com${VM_ID}/instanceView?api-version=2025-04-01" \
  --query "statuses[].{Code:code,Status:displayStatus}" \
  --output table
```

Generare carico:

```bash
az vm run-command invoke \
  --resource-group "$RG_NAME" \
  --name "$VM_NAME" \
  --command-id RunShellScript \
  --scripts "timeout 30s bash -c 'while true; do :; done'" \
  --output json > evidence/ud07_autonomo_vm_runcommand.json
```

Dopo:

```bash
sleep 180

bash src/az_metrics_snapshot.sh "$VM_ID" "Percentage CPU" PT1M "Average Maximum" evidence/ud07_autonomo_vm_cpu_after.json
```

Screenshot:

```text
img/ud07_autonomo_vm_cpu_after.png
```

## 9. Scenario D: Activity Log amministrativo

Eseguire lo script amministrativo:

```bash
# Seguire la PARTE A della guida 04_OBS_UD07_GENERAZIONE_CONTROLLATA_SEGNALI_Passo_Passo.md
```

Dal Portale:

```text
Resource Group
→ Activity log
→ Last hour
```

Screenshot:

```text
img/ud07_autonomo_activity_log_after_admin.png
```

Nel report specificare chiaramente:

```text
Questo scenario genera eventi amministrativi, non traffico applicativo.
```

## 10. Diagnostic Settings

Per la risorsa scelta, recuperare categorie e impostazioni:

```bash
bash src/az_diagnostic_settings_inventory.sh "$RESOURCE_ID" evidence/ud07_autonomo_diagnostic_settings.json evidence/ud07_autonomo_diagnostic_categories.json
```

Se `RESOURCE_ID` non è impostato, ricavarlo dalla risorsa scelta.

Esempio App Service:

```bash
RESOURCE_ID="$APP_ID"
```

Nel report indicare:

```text
categorie disponibili;
Diagnostic Settings esistenti;
proposta di destinazione futura, per esempio Log Analytics Workspace;
limiti o errori incontrati.
```

## 11. Output richiesti

Alla fine devono essere presenti:

```text
docs/report_ud07_autonomo.md
almeno 2 file JSON in evidence/
almeno 1 file log in logs/
almeno 1 screenshot in img/
```

Esempio verifica:

```bash
find docs evidence logs img -maxdepth 2 -type f | sort
```

## 12. Domande finali nel report

Rispondere in modo sintetico:

```text
Quale risorsa hai osservato?
Quale domanda diagnostica hai formulato?
Quale segnale ti aspettavi?
Che cosa hai visto prima?
Che cosa hai visto dopo?
Il segnale era amministrativo o applicativo?
Quale limite hai osservato?
Quale evidenza supporta la tua conclusione?
```

## 13. Commit finale

```bash
git status

git add docs evidence logs img config

git commit -m "Completamento laboratorio autonomo UD07"
```

Se previsto:

```bash
git push
```

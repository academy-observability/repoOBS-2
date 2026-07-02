# 05 - Laboratorio guidato UD08
## Tabelle Azure reali nel Log Analytics Workspace

## Obiettivo

In questa estensione guidata colleghiamo al Log Analytics Workspace della UD08 alcune risorse create nelle UD precedenti, in particolare UD05, per interrogare tabelle Azure reali con KQL.

Il laboratorio principale UD08 usa `datatable()` per garantire query sempre eseguibili anche con workspace vuoto. Questa estensione aggiunge invece una parte realistica: configurazione della raccolta dati, generazione di traffico controllato e interrogazione di tabelle popolate da servizi Azure.

Alla fine avremo:

- recuperato i resource ID delle risorse create in UD05;
- collegato l'Activity Log della subscription al workspace;
- collegato Storage Account Blob service al workspace;
- collegato Web App/App Service al workspace;
- generato attività amministrativa e traffico applicativo controllato;
- interrogato tabelle reali come `AzureActivity`, `StorageBlobLogs`, `AppServiceHTTPLogs`;
- distinto correttamente tabella assente, tabella presente ma vuota, query con errore e ritardo di ingestione;
- salvato evidenze JSON e screenshot.

> Nota didattica: la parte VM con Azure Monitor Agent e Data Collection Rule è inclusa come estensione opzionale perché richiede più tempo operativo e può dipendere dal sistema operativo della VM.

---

## Quando usare questo file

Usare questo file dopo i task base del laboratorio UD08 basati su `datatable()`.

Sequenza consigliata:

```text
01_OBS_UD08_LAB_guidato_Log_Analytics_KQL_Base_v5_2.md
05_OBS_UD08_LAB_guidato_Tabelle_Azure_Reali_v5_3.md
```

Il primo file garantisce l'apprendimento KQL minimo. Questo file introduce le tabelle reali.

---

## Prerequisiti

| Verifica | Comando o azione | Nota |
|---|---|---|
| Workspace UD08 disponibile | `az monitor log-analytics workspace show` | Deve essere in stato `Succeeded` |
| Risorse UD05 disponibili | VM, Storage Account, container, Web App | I nomi possono variare per partecipante |
| Azure CLI autenticata | `az account show -o table` | Usare la subscription corretta |
| Permessi sufficienti | Contributor o Owner sulle risorse | Per diagnostic settings e tag update |
| Cartelle locali presenti | `evidence`, `logs`, `img`, `src/kql/azure` | Create se mancanti |

---

# Task 1 - Preparazione ambiente locale

Eseguire dalla directory `work/UD08` del repository locale.

```bash
mkdir -p evidence logs img src/kql/azure docs
```

Caricare la configurazione UD08:

```bash
set -a
source config/ud08.env
set +a
```

Verificare le variabili minime:

```bash
printf 'SUB_ID=<%s>\nRG=<%s>\nLOCATION=<%s>\nLAW=<%s>\nWORKSPACE_ID=<%s>\n' \
  "$SUB_ID" "$RG" "$LOCATION" "$LAW" "$WORKSPACE_ID"
```

Se `WORKSPACE_ID` è vuoto, recuperarlo dal workspace:

```bash
export WORKSPACE_ID="$(az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --query customerId \
  --output tsv)"

printf 'WORKSPACE_ID=<%s>\n' "$WORKSPACE_ID"
```

Recuperare anche il resource ID completo del workspace. Questo valore serve per configurare i diagnostic settings.

```bash
export LAW_RESOURCE_ID="$(az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --query id \
  --output tsv)"

printf 'LAW_RESOURCE_ID=<%s>\n' "$LAW_RESOURCE_ID" | tee evidence/law_resource_id.txt
```

Verificare che il workspace sia pronto:

```bash
az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW" \
  --query "{name:name,customerId:customerId,location:location,provisioningState:provisioningState}" \
  --output table
```

Il valore atteso per `provisioningState` è:

```text
Succeeded
```

---

# Task 2 - Aggiunta variabili delle risorse UD05

Nel file `config/ud08.env` aggiungere o verificare queste variabili.

```bash
# Risorse create nelle UD precedenti, in particolare UD05.
RG_UD05="rg-obs-ud05-ep"
VM_NAME="<nome-vm-ud05>"
STORAGE_ACCOUNT="<nome-storage-account-ud05>"
CONTAINER_NAME="<nome-container-ud05>"
WEBAPP_NAME="<nome-webapp-ud05>"
```

Ricaricare il file:

```bash
set -a
source config/ud08.env
set +a
```

Verificare:

```bash
printf 'RG_UD05=<%s>\nVM_NAME=<%s>\nSTORAGE_ACCOUNT=<%s>\nCONTAINER_NAME=<%s>\nWEBAPP_NAME=<%s>\n' \
  "$RG_UD05" "$VM_NAME" "$STORAGE_ACCOUNT" "$CONTAINER_NAME" "$WEBAPP_NAME"
```

Se non ricordiamo i nomi delle risorse, elencarle:

```bash
az resource list \
  --resource-group "$RG_UD05" \
  --query "[].{name:name,type:type,location:location}" \
  --output table
```

Salvare l'elenco come evidenza:

```bash
az resource list \
  --resource-group "$RG_UD05" \
  --output json > evidence/ud05_resources_list.json
```

---

# Task 3 - Test di base: il motore KQL risponde?

Prima di lavorare sulle tabelle reali, verifichiamo che la CLI riesca a interrogare il workspace.

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "datatable(x:int, msg:string)[1, 'cli ok']" \
  --output jsonc
```

Risultato atteso:

```json
[
  {
    "TableName": "PrimaryResult",
    "msg": "cli ok",
    "x": "1"
  }
]
```

Se questa query fallisce, il problema non riguarda le tabelle Azure reali. Verificare login, subscription, permessi e `WORKSPACE_ID`.

---

# Task 4 - Activity Log della subscription verso Log Analytics

## 4.1 Perché partiamo da AzureActivity

`AzureActivity` è una delle tabelle più utili per il laboratorio perché contiene attività amministrative Azure: creazione, modifica, eliminazione, aggiornamento tag, restart servizi, start/stop VM, operazioni ARM.

Questa tabella diventa disponibile nel workspace quando esportiamo l'Activity Log della subscription verso Log Analytics.

## 4.2 Creare diagnostic setting a livello subscription

Creare il diagnostic setting della subscription:

```bash
az monitor diagnostic-settings subscription create \
  --name "ds-ud08-activity-to-law" \
  --location "$LOCATION" \
  --workspace "$LAW_RESOURCE_ID" \
  --logs '[
    {"category":"Administrative","enabled":true},
    {"category":"Security","enabled":true},
    {"category":"ServiceHealth","enabled":true},
    {"category":"Alert","enabled":true},
    {"category":"Recommendation","enabled":true},
    {"category":"Policy","enabled":true},
    {"category":"Autoscale","enabled":true},
    {"category":"ResourceHealth","enabled":true}
  ]' \
  --output json > evidence/activitylog_diagnostic_setting_create.json
```

Verificare:

```bash
az monitor diagnostic-settings subscription list \
  --output table
```

Salvare evidenza:

```bash
az monitor diagnostic-settings subscription list \
  --output json > evidence/activitylog_diagnostic_settings_list.json
```

## 4.3 Generare un evento amministrativo controllato

Aggiorniamo un tag del Resource Group UD05. Questa operazione genera attività amministrativa tracciabile.

```bash
az group update \
  --name "$RG_UD05" \
  --set tags.ud08ActivityTest="$(date +%s)" \
  --output json > evidence/ud08_activity_rg_tag_update.json
```

## 4.4 Query KQL su AzureActivity

Creare il file:

```bash
cat > src/kql/azure/10_azureactivity_ud05_recent.kql <<'EOF'
// UD08 - AzureActivity su risorse UD05
// Mostra attività amministrative recenti nel Resource Group del laboratorio.
AzureActivity
| where TimeGenerated > ago(2h)
| where ResourceGroup =~ "rg-obs-ud05-ep"
| project TimeGenerated, OperationNameValue, ActivityStatusValue, ResourceGroup, ResourceProviderValue, Caller
| sort by TimeGenerated desc
| take 30
EOF
```

Se il Resource Group dei partecipanti ha un nome diverso, modificare la riga:

```kusto
| where ResourceGroup =~ "rg-obs-ud05-ep"
```

Eseguire da CLI:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/10_azureactivity_ud05_recent.kql)" \
  --timespan PT2H \
  --output json > evidence/query_azureactivity_ud05_recent.json
```

Verificare:

```bash
python3 -m json.tool evidence/query_azureactivity_ud05_recent.json | head -120
```

## 4.5 Query diagnostica con count

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "AzureActivity | where TimeGenerated > ago(2h) | count" \
  --timespan PT2H \
  --output json > evidence/query_azureactivity_count.json

cat evidence/query_azureactivity_count.json
```

Se `Count` è `0`, attendere qualche minuto e riprovare. L'ingestione non è sempre immediata.

---

# Task 5 - Storage Account Blob logs verso Log Analytics

## 5.1 Obiettivo

Colleghiamo il servizio Blob dello Storage Account UD05 al LAW. Poi generiamo traffico controllato sul container: upload, list, download, delete.

La tabella attesa, in modalità resource-specific, è:

```text
StorageBlobLogs
```

## 5.2 Recuperare resource ID dello Storage Account e del Blob service

```bash
export STG_ID="$(az storage account show \
  --resource-group "$RG_UD05" \
  --name "$STORAGE_ACCOUNT" \
  --query id \
  --output tsv)"

export BLOB_SERVICE_ID="${STG_ID}/blobServices/default"

printf 'STG_ID=<%s>\nBLOB_SERVICE_ID=<%s>\n' "$STG_ID" "$BLOB_SERVICE_ID" \
  | tee evidence/storage_resource_ids.txt
```

## 5.3 Verificare le categorie diagnostiche disponibili

```bash
az monitor diagnostic-settings categories list \
  --resource "$BLOB_SERVICE_ID" \
  --output table
```

Salvare evidenza:

```bash
az monitor diagnostic-settings categories list \
  --resource "$BLOB_SERVICE_ID" \
  --output json > evidence/storage_blob_diagnostic_categories.json
```

## 5.4 Creare diagnostic setting per Blob service

```bash
az monitor diagnostic-settings create \
  --name "ds-ud08-blob-to-law" \
  --resource "$BLOB_SERVICE_ID" \
  --workspace "$LAW_RESOURCE_ID" \
  --export-to-resource-specific true \
  --logs '[
    {"category":"StorageRead","enabled":true},
    {"category":"StorageWrite","enabled":true},
    {"category":"StorageDelete","enabled":true}
  ]' \
  --output json > evidence/storage_blob_diagnostic_setting_create.json
```

Verificare:

```bash
az monitor diagnostic-settings list \
  --resource "$BLOB_SERVICE_ID" \
  --output table
```

## 5.5 Generare traffico Blob

Creare un file locale:

```bash
echo "UD08 storage test $(date -Is)" > logs/ud08-storage-test.txt
export BLOB_NAME="ud08-test-$(date +%s).txt"
```

Upload:

```bash
az storage blob upload \
  --account-name "$STORAGE_ACCOUNT" \
  --container-name "$CONTAINER_NAME" \
  --name "$BLOB_NAME" \
  --file logs/ud08-storage-test.txt \
  --auth-mode login \
  --overwrite \
  --output json > evidence/storage_blob_upload.json
```

List:

```bash
az storage blob list \
  --account-name "$STORAGE_ACCOUNT" \
  --container-name "$CONTAINER_NAME" \
  --auth-mode login \
  --output json > evidence/storage_blob_list.json
```

Download:

```bash
az storage blob download \
  --account-name "$STORAGE_ACCOUNT" \
  --container-name "$CONTAINER_NAME" \
  --name "$BLOB_NAME" \
  --file "logs/downloaded-$BLOB_NAME" \
  --auth-mode login \
  --output json > evidence/storage_blob_download.json
```

Delete:

```bash
az storage blob delete \
  --account-name "$STORAGE_ACCOUNT" \
  --container-name "$CONTAINER_NAME" \
  --name "$BLOB_NAME" \
  --auth-mode login \
  --output json > evidence/storage_blob_delete.json
```

Se i comandi falliscono con errore di autorizzazione, verificare che l'utente abbia un ruolo dati come `Storage Blob Data Contributor` sullo Storage Account o sul container. In alternativa, per il solo laboratorio docente, usare connection string senza salvarla nel repository.

## 5.6 Query KQL su StorageBlobLogs

Creare il file:

```bash
cat > src/kql/azure/11_storagebloblogs_ud05_recent.kql <<'EOF'
// UD08 - StorageBlobLogs su Storage Account UD05
// Mostra operazioni recenti sul servizio Blob.
StorageBlobLogs
| where TimeGenerated > ago(2h)
| project TimeGenerated, AccountName, OperationName, StatusText, DurationMs, Uri, CallerIpAddress
| sort by TimeGenerated desc
| take 50
EOF
```

Eseguire:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/11_storagebloblogs_ud05_recent.kql)" \
  --timespan PT2H \
  --output json > evidence/query_storagebloblogs_ud05_recent.json
```

Verificare:

```bash
python3 -m json.tool evidence/query_storagebloblogs_ud05_recent.json | head -120
```

Query di conteggio:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "StorageBlobLogs | where TimeGenerated > ago(2h) | count" \
  --timespan PT2H \
  --output json > evidence/query_storagebloblogs_count.json

cat evidence/query_storagebloblogs_count.json
```

---

# Task 6 - Web App/App Service logs verso Log Analytics

## 6.1 Obiettivo

Colleghiamo la Web App creata in UD05 al LAW e generiamo richieste HTTP controllate.

La tabella più interessante per questo laboratorio è:

```text
AppServiceHTTPLogs
```

Altre tabelle possibili, a seconda della configurazione, sono:

```text
AppServiceConsoleLogs
AppServiceAppLogs
AppServiceAuditLogs
AppServicePlatformLogs
```

## 6.2 Recuperare resource ID della Web App

```bash
export WEBAPP_ID="$(az webapp show \
  --resource-group "$RG_UD05" \
  --name "$WEBAPP_NAME" \
  --query id \
  --output tsv)"

printf 'WEBAPP_ID=<%s>\n' "$WEBAPP_ID" | tee evidence/webapp_resource_id.txt
```

## 6.3 Verificare categorie disponibili

```bash
az monitor diagnostic-settings categories list \
  --resource "$WEBAPP_ID" \
  --output table
```

Salvare evidenza:

```bash
az monitor diagnostic-settings categories list \
  --resource "$WEBAPP_ID" \
  --output json > evidence/webapp_diagnostic_categories.json
```

## 6.4 Creare diagnostic setting per Web App

Usare prima questa versione con le categorie più comuni.

```bash
az monitor diagnostic-settings create \
  --name "ds-ud08-webapp-to-law" \
  --resource "$WEBAPP_ID" \
  --workspace "$LAW_RESOURCE_ID" \
  --export-to-resource-specific true \
  --logs '[
    {"category":"AppServiceHTTPLogs","enabled":true},
    {"category":"AppServiceConsoleLogs","enabled":true},
    {"category":"AppServiceAppLogs","enabled":true},
    {"category":"AppServiceAuditLogs","enabled":true},
    {"category":"AppServicePlatformLogs","enabled":true}
  ]' \
  --output json > evidence/webapp_diagnostic_setting_create.json
```

Se il comando fallisce perché una categoria non è supportata, leggere l'elenco prodotto al punto precedente e ripetere il comando includendo solo le categorie disponibili.

Versione minima, se disponibile solo `AppServiceHTTPLogs`:

```bash
az monitor diagnostic-settings create \
  --name "ds-ud08-webapp-to-law" \
  --resource "$WEBAPP_ID" \
  --workspace "$LAW_RESOURCE_ID" \
  --export-to-resource-specific true \
  --logs '[
    {"category":"AppServiceHTTPLogs","enabled":true}
  ]' \
  --output json > evidence/webapp_diagnostic_setting_create.json
```

Verificare:

```bash
az monitor diagnostic-settings list \
  --resource "$WEBAPP_ID" \
  --output table
```

## 6.5 Generare traffico HTTP

```bash
for i in {1..20}; do
  curl -s -o /dev/null -w "request=$i status=%{http_code} time=%{time_total}\n" \
    "https://${WEBAPP_NAME}.azurewebsites.net/?ud08=$i"
done | tee evidence/webapp_curl_ok.txt
```

Generare anche una richiesta verso un percorso inesistente, utile per osservare un eventuale `404`:

```bash
curl -s -o /dev/null -w "status=%{http_code} time=%{time_total}\n" \
  "https://${WEBAPP_NAME}.azurewebsites.net/not-found-ud08" \
  | tee evidence/webapp_curl_404.txt
```

## 6.6 Query KQL su AppServiceHTTPLogs

Creare il file:

```bash
cat > src/kql/azure/12_appservicehttplogs_ud05_recent.kql <<'EOF'
// UD08 - AppServiceHTTPLogs su Web App UD05
// Mostra richieste HTTP recenti ricevute dalla Web App.
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| project TimeGenerated, CsMethod, CsUriStem, ScStatus, TimeTaken, CIp, UserAgent, _ResourceId
| sort by TimeGenerated desc
| take 50
EOF
```

Eseguire:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/12_appservicehttplogs_ud05_recent.kql)" \
  --timespan PT2H \
  --output json > evidence/query_appservicehttplogs_ud05_recent.json
```

Verificare:

```bash
python3 -m json.tool evidence/query_appservicehttplogs_ud05_recent.json | head -120
```

Query di conteggio:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "AppServiceHTTPLogs | where TimeGenerated > ago(2h) | count" \
  --timespan PT2H \
  --output json > evidence/query_appservicehttplogs_count.json

cat evidence/query_appservicehttplogs_count.json
```

---

# Task 7 - Query riepilogativa sulle tabelle reali

Dopo aver configurato Activity Log, Storage e Web App, attendere alcuni minuti e poi verificare quali tabelle hanno ricevuto righe.

Creare il file:

```bash
cat > src/kql/azure/13_realtables_summary_ud08.kql <<'EOF'
// UD08 - Riepilogo tabelle reali attese
// isfuzzy=true permette alla query di proseguire anche se alcune tabelle non esistono ancora.
union isfuzzy=true
    AzureActivity,
    StorageBlobLogs,
    AppServiceHTTPLogs,
    Heartbeat,
    Perf,
    Syslog,
    Event
| where TimeGenerated > ago(2h)
| summarize Righe=count() by Type
| sort by Righe desc
EOF
```

Eseguire:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "$(cat src/kql/azure/13_realtables_summary_ud08.kql)" \
  --timespan PT2H \
  --output json > evidence/query_realtables_summary_ud08.json

python3 -m json.tool evidence/query_realtables_summary_ud08.json | head -120
```

Se il risultato è vuoto, non concludere immediatamente che la configurazione sia errata. Verificare:

- diagnostic setting creato sulla risorsa corretta;
- destinazione LAW corretta;
- categoria log abilitata;
- traffico generato dopo la creazione del diagnostic setting;
- time range adeguato;
- attesa sufficiente per ingestione.

---

# Task 8 - VM con Azure Monitor Agent e Data Collection Rule opzionale

## 8.1 Perché opzionale

Per la VM non usiamo la vecchia diagnostica legacy. Usiamo il modello corretto:

```text
Azure Monitor Agent + Data Collection Rule + associazione alla VM
```

Questa parte è didatticamente importante, ma può richiedere più tempo rispetto a Storage e Web App.

## 8.2 Procedura consigliata da Portale

```text
Azure Portal
-> Monitor
-> Data Collection Rules
-> Create
```

Impostazioni suggerite:

```text
Nome: dcr-ud08-vm-basic
Resource group: rg-obs-ud05-ep
Region: stessa regione della VM o del workspace
Resources: selezionare la VM UD05
Destination: Log Analytics Workspace law-obs-ud08-ep
```

Data sources per VM Linux:

```text
Syslog: auth, authpriv, daemon, syslog
Performance counters: CPU, Memory, Disk, Network
```

Data sources per VM Windows:

```text
Windows Event Logs: System, Application
Performance counters: CPU, Memory, Disk, Network
```

Tabelle attese:

| VM | Tabelle |
|---|---|
| Linux | `Heartbeat`, `Perf`, `Syslog` |
| Windows | `Heartbeat`, `Perf`, `Event` |

## 8.3 Query KQL per VM

Heartbeat:

```kusto
Heartbeat
| where TimeGenerated > ago(2h)
| project TimeGenerated, Computer, OSType, ResourceGroup, _ResourceId
| sort by TimeGenerated desc
| take 20
```

Performance counters:

```kusto
Perf
| where TimeGenerated > ago(2h)
| summarize AvgValue=avg(CounterValue) by Computer, ObjectName, CounterName, bin(TimeGenerated, 5m)
| sort by TimeGenerated desc
| take 50
```

Linux Syslog:

```kusto
Syslog
| where TimeGenerated > ago(2h)
| project TimeGenerated, Computer, Facility, SeverityLevel, SyslogMessage
| sort by TimeGenerated desc
| take 30
```

Windows Event Log:

```kusto
Event
| where TimeGenerated > ago(2h)
| project TimeGenerated, Computer, EventLog, EventID, Source, RenderedDescription
| sort by TimeGenerated desc
| take 30
```

---

# Task 9 - Troubleshooting guidato

## Caso A - Query `Usage | count` restituisce 0

Significa che la query è valida ma nel periodo indicato non ci sono record in `Usage`.

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "Usage | count" \
  --timespan P7D \
  --output jsonc
```

Da documentare come:

```text
Tabella interrogabile, ma senza righe nel timespan selezionato.
```

## Caso B - Query su tabella reale restituisce `[]`

Esempio:

```json
[]
```

Significa risultato valido ma senza righe. Verificare count, time range e ingestione.

## Caso C - Errore `Failed to resolve table or column expression`

Significa che la tabella non esiste ancora nel workspace oppure non è stata popolata almeno una volta.

Azioni:

- verificare diagnostic setting;
- generare traffico;
- attendere ingestione;
- controllare se la modalità è `resource-specific` oppure `AzureDiagnostics`.

## Caso D - File JSON a 0 byte

Un file a 0 byte non è un risultato KQL vuoto. Di solito indica comando fallito o errore scritto su `stderr`.

Usare sempre una forma robusta:

```bash
az monitor log-analytics query \
  --workspace "$WORKSPACE_ID" \
  --analytics-query "AppServiceHTTPLogs | count" \
  --timespan PT2H \
  --output json \
  > evidence/test.json \
  2> logs/test.err

EXIT_CODE=$?
echo "EXIT_CODE=$EXIT_CODE"
ls -lh evidence/test.json
cat logs/test.err
```

## Caso E - Diagnostic setting creato ma nessun dato

Verificare:

```bash
az monitor diagnostic-settings list --resource "$WEBAPP_ID" --output table
az monitor diagnostic-settings list --resource "$BLOB_SERVICE_ID" --output table
az monitor diagnostic-settings subscription list --output table
```

Poi rigenerare traffico e aumentare il time range:

```kusto
AppServiceHTTPLogs
| where TimeGenerated > ago(24h)
| take 20
```

---

# Task 10 - Evidenze richieste

Salvare almeno queste evidenze:

| Evidenza | File |
|---|---|
| Resource ID LAW | `evidence/law_resource_id.txt` |
| Lista risorse UD05 | `evidence/ud05_resources_list.json` |
| Diagnostic setting Activity Log | `evidence/activitylog_diagnostic_setting_create.json` |
| Query AzureActivity | `evidence/query_azureactivity_ud05_recent.json` |
| Diagnostic setting Storage Blob | `evidence/storage_blob_diagnostic_setting_create.json` |
| Traffico Blob | `evidence/storage_blob_upload.json`, `storage_blob_list.json`, `storage_blob_download.json`, `storage_blob_delete.json` |
| Query StorageBlobLogs | `evidence/query_storagebloblogs_ud05_recent.json` |
| Diagnostic setting Web App | `evidence/webapp_diagnostic_setting_create.json` |
| Traffico Web App | `evidence/webapp_curl_ok.txt`, `evidence/webapp_curl_404.txt` |
| Query AppServiceHTTPLogs | `evidence/query_appservicehttplogs_ud05_recent.json` |
| Riepilogo tabelle reali | `evidence/query_realtables_summary_ud08.json` |
| Screenshot portale Logs | `img/ud08_logs_tabelle_reali.png` |

---

# Task 11 - Sezione da inserire nel report

Aggiungere al report guidato una sezione simile:

```markdown
## Tabelle Azure reali collegate al LAW

### Risorse integrate

| Risorsa | Diagnostic setting / DCR | Tabella attesa | Esito |
|---|---|---|---|
| Activity Log subscription | ds-ud08-activity-to-law | AzureActivity | ... |
| Storage Account Blob service | ds-ud08-blob-to-law | StorageBlobLogs | ... |
| Web App | ds-ud08-webapp-to-law | AppServiceHTTPLogs | ... |
| VM | DCR + AMA | Heartbeat / Perf / Syslog / Event | opzionale |

### Osservazioni

- Il workspace non contiene automaticamente dati reali solo perché è stato creato.
- Le tabelle reali compaiono quando almeno una sorgente invia dati al workspace.
- `datatable()` è indipendente dai dati del workspace.
- `Usage | count` può restituire 0 anche se il workspace è valido.
- Un risultato `[]` è diverso da un file JSON a 0 byte.
- Il ritardo di ingestione va considerato nella diagnosi.
```

---

# Task 12 - Verifica finale e commit

```bash
find evidence logs img src/kql/azure -maxdepth 3 -type f | sort

git status
```

Commit consigliato:

```bash
git add evidence logs img src/kql/azure docs config/ud08.env.example *.md

git commit -m "UD08 integrazione tabelle Azure reali da risorse UD05"

git push
```

---

## Criteri di completamento

| Criterio | Stato |
|---|---|
| Workspace ID e LAW resource ID verificati | ☐ |
| Risorse UD05 individuate | ☐ |
| Activity Log collegato al LAW | ☐ |
| Evento amministrativo generato | ☐ |
| Query `AzureActivity` eseguita | ☐ |
| Storage Blob diagnostic setting creato | ☐ |
| Traffico Blob generato | ☐ |
| Query `StorageBlobLogs` eseguita | ☐ |
| Web App diagnostic setting creato | ☐ |
| Traffico HTTP generato | ☐ |
| Query `AppServiceHTTPLogs` eseguita | ☐ |
| Risultati vuoti documentati correttamente | ☐ |
| Evidenze salvate | ☐ |
| Report aggiornato | ☐ |
| Commit/push eseguito | ☐ |

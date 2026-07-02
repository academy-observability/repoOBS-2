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
01_OBS_UD08_LAB_guidato_Log_Analytics_KQL_Base_v5_3.md
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


> Coerenza didattica: ogni partecipante deve collegare al proprio LAW UD08 le proprie risorse UD05. I nomi riportati dal docente, ad esempio storage, VM o Web App del docente, devono essere trattati solo come esempi di output e non devono essere copiati nel file `config/ud08.env` dei partecipanti.

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

# Task 2 - Individuazione delle risorse UD05 del partecipante

## 2.1 Regola importante

In questa sezione non dobbiamo copiare i nomi delle risorse del docente. Ogni partecipante deve individuare le proprie risorse UD05 e usare quelle nel proprio `config/ud08.env`.

Per il docente, un inventario reale potrebbe essere simile a questo:

```text
Storage Account: stobsud05ep01
Web App:         app-obs-ud05-ep
VM:              vm01
LAW UD08:        law-obs-ud08-ep
```

Questi valori servono solo come esempio di forma. Nel laboratorio dei partecipanti devono essere sostituiti dai valori della loro subscription o del loro resource group.

## 2.2 Individuare il Resource Group UD05 corretto

Elencare i Resource Group disponibili e individuare quello creato durante UD05:

```bash
az group list \
  --query "[].{name:name,location:location}" \
  --output table
```

Impostare il Resource Group UD05 del partecipante:

```bash
export RG_UD05="<resource-group-ud05-del-partecipante>"
```

Esempio docente, da non copiare nei repository dei partecipanti:

```bash
# export RG_UD05="rg-obs-ud05-ep"
```

## 2.3 Creare l'inventario delle risorse UD05

```bash
az resource list \
  --resource-group "$RG_UD05" \
  --query "[].{name:name,type:type,location:location}" \
  --output table
```

Salvare l'inventario come evidenza:

```bash
az resource list \
  --resource-group "$RG_UD05" \
  --output json > evidence/ud05_resources_list.json
```

Per ridurre gli errori, estraiamo solo le risorse usate in questo laboratorio:

```bash
az resource list \
  --resource-group "$RG_UD05" \
  --query "[?type=='Microsoft.Storage/storageAccounts' || type=='Microsoft.Web/sites' || type=='Microsoft.Compute/virtualMachines'].{name:name,type:type,location:location}" \
  --output table
```

## 2.4 Derivare automaticamente Storage Account, Web App e VM

Se nel Resource Group UD05 c'è una sola risorsa per tipo, possiamo valorizzare le variabili automaticamente:

```bash
export STORAGE_ACCOUNT="$(az storage account list \
  --resource-group "$RG_UD05" \
  --query "[0].name" \
  --output tsv)"

export WEBAPP_NAME="$(az webapp list \
  --resource-group "$RG_UD05" \
  --query "[0].name" \
  --output tsv)"

export VM_NAME="$(az vm list \
  --resource-group "$RG_UD05" \
  --query "[0].name" \
  --output tsv)"
```

Se il Resource Group contiene più Storage Account, più Web App o più VM, non usare l'indice `[0]` alla cieca: scegliere la risorsa corretta dalla tabella del punto precedente e valorizzare manualmente la variabile.

## 2.5 Individuare il container Blob

Il container non compare nell'elenco `az resource list`, perché è un oggetto dati del servizio Blob. Elencarlo separatamente:

```bash
az storage container list \
  --account-name "$STORAGE_ACCOUNT" \
  --auth-mode login \
  --query "[].name" \
  --output table
```

Se esiste un solo container di laboratorio:

```bash
export CONTAINER_NAME="$(az storage container list \
  --account-name "$STORAGE_ACCOUNT" \
  --auth-mode login \
  --query "[0].name" \
  --output tsv)"
```

Se il comando fallisce con un errore di autorizzazione, significa che l'utente può vedere la risorsa Azure ma non ha ancora i permessi dati sul Blob. In quel caso verificare il ruolo `Storage Blob Data Contributor`, oppure leggere temporaneamente il nome del container dal Portale Azure e valorizzare manualmente:

```bash
export CONTAINER_NAME="<nome-container-ud05-del-partecipante>"
```

## 2.6 Scrivere le variabili nel file `config/ud08.env`

Aggiungere o aggiornare queste righe nel file `config/ud08.env`:

```bash
# Risorse UD05 del partecipante da osservare tramite il LAW UD08.
RG_UD05="<resource-group-ud05-del-partecipante>"
VM_NAME="<vm-ud05-del-partecipante>"
STORAGE_ACCOUNT="<storage-account-ud05-del-partecipante>"
CONTAINER_NAME="<container-blob-ud05-del-partecipante>"
WEBAPP_NAME="<web-app-ud05-del-partecipante>"
WEBAPP_HOST=""
```

Non inserire chiavi, connection string, SAS token o password nel file di configurazione.

Ricaricare il file:

```bash
set -a
source config/ud08.env
set +a
```

## 2.7 Validare che le variabili puntino a risorse esistenti

```bash
printf 'RG_UD05=<%s>\nVM_NAME=<%s>\nSTORAGE_ACCOUNT=<%s>\nCONTAINER_NAME=<%s>\nWEBAPP_NAME=<%s>\n' \
  "$RG_UD05" "$VM_NAME" "$STORAGE_ACCOUNT" "$CONTAINER_NAME" "$WEBAPP_NAME"
```

Controllare che Storage Account, Web App e VM esistano davvero nel Resource Group indicato:

```bash
az storage account show \
  --resource-group "$RG_UD05" \
  --name "$STORAGE_ACCOUNT" \
  --query "{name:name,location:location,kind:kind}" \
  --output table

az webapp show \
  --resource-group "$RG_UD05" \
  --name "$WEBAPP_NAME" \
  --query "{name:name,location:location,state:state,defaultHostName:defaultHostName}" \
  --output table

az vm show \
  --resource-group "$RG_UD05" \
  --name "$VM_NAME" \
  --query "{name:name,location:location,powerState:powerState}" \
  --show-details \
  --output table
```

Salvare le variabili rilevate come evidenza:

```bash
cat > evidence/ud08_resource_variables_detected.txt <<EOF
RG_UD05=$RG_UD05
VM_NAME=$VM_NAME
STORAGE_ACCOUNT=$STORAGE_ACCOUNT
CONTAINER_NAME=$CONTAINER_NAME
WEBAPP_NAME=$WEBAPP_NAME
LAW=$LAW
WORKSPACE_ID=$WORKSPACE_ID
LAW_RESOURCE_ID=$LAW_RESOURCE_ID
EOF

cat evidence/ud08_resource_variables_detected.txt
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

Il file è già presente nel pacchetto:

```text
src/kql/azure/10_azureactivity_ud05_recent.kql
```

Aprire il file e, se necessario, valorizzare la variabile KQL `ResourceGroupName`. Se il valore resta vuoto, la query mostra le attività recenti visibili nel workspace senza limitarsi a un solo Resource Group.

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

Se i comandi falliscono con errore di autorizzazione, verificare che l'utente abbia un ruolo dati come `Storage Blob Data Contributor` sullo Storage Account o sul container. In alternativa, documentare il prerequisito mancante e completare il laboratorio con le altre sorgenti disponibili. Non salvare connection string o chiavi nel repository.

## 5.6 Query KQL su StorageBlobLogs

Il file è già presente nel pacchetto:

```text
src/kql/azure/11_storagebloblogs_ud05_recent.kql
```

Aprire il file e, se necessario, valorizzare la variabile KQL `StorageAccountName`. Se il valore resta vuoto, la query mostra le operazioni Blob recenti visibili nel workspace.

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

Recuperare l'host reale della Web App. Non costruire l'URL a mano: alcuni App Service usano hostname regionali diversi dal formato semplice `nome.azurewebsites.net`.

```bash
export WEBAPP_HOST="$(az webapp show \
  --resource-group "$RG_UD05" \
  --name "$WEBAPP_NAME" \
  --query defaultHostName \
  --output tsv)"

printf 'WEBAPP_HOST=<%s>\n' "$WEBAPP_HOST" | tee evidence/webapp_host.txt
```

Generare richieste HTTP controllate:

```bash
for i in {1..20}; do
  curl -s -o /dev/null -w "request=$i status=%{http_code} time=%{time_total}\n" \
    "https://${WEBAPP_HOST}/?ud08=$i"
done | tee evidence/webapp_curl_ok.txt
```

Generare anche una richiesta verso un percorso inesistente, utile per osservare un eventuale `404`:

```bash
curl -s -o /dev/null -w "status=%{http_code} time=%{time_total}\n" \
  "https://${WEBAPP_HOST}/not-found-ud08" \
  | tee evidence/webapp_curl_404.txt
```

## 6.6 Query KQL su AppServiceHTTPLogs

Il file è già presente nel pacchetto:

```text
src/kql/azure/12_appservicehttplogs_ud05_recent.kql
```

Aprire il file e, se necessario, valorizzare la variabile KQL `WebAppName`. Se il valore resta vuoto, la query mostra le richieste App Service recenti visibili nel workspace.

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

Usare il file già presente nel pacchetto:

```text
src/kql/azure/13_realtables_summary_ud08.kql
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
Resource group: valore di RG_UD05 del partecipante
Region: preferibilmente la regione della VM o la regione richiesta dalla configurazione guidata del Portale
Resources: selezionare la VM indicata da VM_NAME
Destination: Log Analytics Workspace indicato da LAW
```

Nel caso del docente, con l'inventario mostrato in aula, la VM `vm01` è in `italynorth` mentre il workspace `law-obs-ud08-ep` è in `westeurope`. Questo non deve diventare un valore fisso nel materiale: i partecipanti devono usare le regioni e i nomi effettivi delle proprie risorse.

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

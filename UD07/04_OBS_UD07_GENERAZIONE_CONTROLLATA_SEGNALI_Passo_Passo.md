# OBS UD07 - Generazione controllata di segnali osservabili

## Guida passo dopo passo, senza script `.sh`

Questa guida sostituisce l'esecuzione dei due script:

```text
src/ud07_generate_administrative_activity.sh
src/ud07_generate_application_traffic.sh
```

L'obiettivo è far eseguire ai partecipanti, **comando dopo comando**, le stesse attività prodotte dagli script, in modo più trasparente e più didattico.

La logica è semplice:

```text
1. Osserviamo una baseline.
2. Generiamo attività amministrativa controllata.
3. Verifichiamo Activity Log e tag.
4. Generiamo traffico applicativo e workload controllato.
5. Verifichiamo metriche Azure Monitor.
6. Salviamo evidenze locali.
7. Interpretiamo cosa è cambiato.
```

> Nota operativa: tutti i comandi che scrivono in `logs/`, `evidence/` o `docs/` devono essere eseguiti da WSL o da terminale locale, dentro il repository UD07. Cloud Shell può essere usata per verifiche rapide, ma non deve essere usata per produrre i file del repository locale.

---

## 1. Prerequisiti

Prima di iniziare devono esistere le risorse create nelle UD precedenti:

```text
Resource Group
Storage Account
App Service
Virtual Machine, se presente
```

I partecipanti devono avere:

```text
Azure CLI funzionante;
login Azure già eseguito;
subscription corretta selezionabile;
cartella di lavoro UD07 aperta nel terminale locale;
permessi sufficienti sulle risorse del Resource Group.
```

---

## 2. Preparazione ambiente locale

Eseguire da terminale locale, nella cartella `work/UD07`.

```bash
# Creiamo le cartelle usate per log locali, evidenze e file temporanei.
mkdir -p logs evidence tmp
```

Verificare di essere nella cartella giusta:

```bash
# Mostra la cartella corrente.
pwd

# Mostra le cartelle operative attese.
ls -ld logs evidence tmp
```

---

## 3. Configurazione variabili

Ogni partecipante deve usare i propri nomi risorsa. I valori seguenti sono un esempio e vanno adattati.

```bash
# Subscription Azure usata nel laboratorio.
export SUB_ID="<ID_SUBSCRIPTION>"

# Resource Group creato in UD05.
export RG_NAME="<NOME_RESOURCE_GROUP>"

# Risorse principali create nelle UD precedenti.
export STORAGE_NAME="<NOME_STORAGE_ACCOUNT>"
export APP_NAME="<NOME_APP_SERVICE>"
export VM_NAME="<NOME_VM>"
```

Esempio docente, da non copiare automaticamente se si lavora su risorse personali diverse:

```bash
# Esempio basato su ambiente docente.
export SUB_ID="e2739ea7-945f-4290-940a-b756fadec39d"
export RG_NAME="rg-obs-ud05-ep"
export STORAGE_NAME="stobsud05ep01"
export APP_NAME="app-obs-ud05-ep"
export VM_NAME="vm01"
```

Impostare la subscription:

```bash
# Forziamo Azure CLI a usare la subscription corretta.
az account set --subscription "$SUB_ID"
```

Verificare il contesto:

```bash
# Verifica account, subscription e utente autenticato.
az account show \
  --query "{subscription:name,id:id,user:user.name}" \
  --output table
```

Domanda docente:

```text
La subscription mostrata dalla CLI coincide con quella usata nel Portale Azure?
```

Risposta attesa:

```text
Sì. Nome o ID della subscription coincidono.
```

---

## 4. Verifica inventario risorse

```bash
# Elenca le risorse presenti nel Resource Group.
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{Name:name,Type:type,Location:location}" \
  --output table
```

Salvare l'inventario:

```bash
# Salva l'inventario risorse in evidence/.
az resource list \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud07_resource_inventory_before_generation.json
```

---

## 5. Recupero Resource ID delle risorse core

Non aggiorniamo tag sull'App Service Plan. Alcune SKU, in particolare in scenari Free/F1, possono generare errori poco utili. In questo laboratorio usiamo solo le tre risorse core:

```text
Storage Account
App Service
Virtual Machine
```

```bash
# Recupera il Resource ID dello Storage Account.
export STORAGE_ID="$(az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

```bash
# Recupera il Resource ID dell'App Service.
export APP_ID="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

```bash
# Recupera il Resource ID della VM.
# Se la VM non esiste o non è stata creata in UD05, questo comando può fallire.
export VM_ID="$(az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

Verificare i valori:

```bash
# Mostra gli ID recuperati.
printf 'STORAGE_ID=%s\n' "$STORAGE_ID"
printf 'APP_ID=%s\n' "$APP_ID"
printf 'VM_ID=%s\n' "$VM_ID"
```

Salvare gli ID:

```bash
# Salva gli ID risorsa principali in un file di evidenza.
cat > evidence/ud07_core_resource_ids.txt <<EOF
STORAGE_ID=$STORAGE_ID
APP_ID=$APP_ID
VM_ID=$VM_ID
EOF
```

---

# PARTE A - Generazione di attività amministrativa

Questa parte genera eventi nel **piano di controllo Azure**. L'effetto atteso è:

```text
Activity Log aggiornato;
tag modificati sulle risorse;
nessun traffico applicativo generato.
```

---

## 6. Creazione lista risorse core

```bash
# Scrive in un file solo le risorse core su cui faremo aggiornamento tag.
printf "%s\n%s\n%s\n" "$STORAGE_ID" "$APP_ID" "$VM_ID" > logs/ud07_admin_resource_ids_core.txt
```

Verificare:

```bash
# Controlla quali risorse saranno aggiornate.
cat logs/ud07_admin_resource_ids_core.txt
```

Il file non deve contenere risorse di tipo:

```text
Microsoft.Web/serverFarms
```

Domanda docente:

```text
Perché non aggiorniamo l'App Service Plan in questo esercizio?
```

Risposta attesa:

```text
Perché non ci serve per generare segnali utili e può generare errori legati alla SKU. Usiamo risorse più controllabili.
```

---

## 7. Primo aggiornamento tag, esecuzione esplicita

Questa prima esecuzione è intenzionalmente esplicita. Serve a far vedere che un aggiornamento tag è un'operazione amministrativa sulla risorsa.

```bash
# Identificativo logico della prova amministrativa.
export ADMIN_RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
```

Aggiornare tag sullo Storage Account:

```bash
# Aggiorna tag sullo Storage Account.
az tag update \
  --resource-id "$STORAGE_ID" \
  --operation Merge \
  --tags \
    "ud07AdminProbe=manual-1" \
    "ud07AdminRunId=$ADMIN_RUN_ID" \
    "ud07LastAdminProbe=$(date -u +%Y%m%dT%H%M%SZ)" \
  --output none
```

Aggiornare tag sull'App Service:

```bash
# Aggiorna tag sull'App Service.
az tag update \
  --resource-id "$APP_ID" \
  --operation Merge \
  --tags \
    "ud07AdminProbe=manual-1" \
    "ud07AdminRunId=$ADMIN_RUN_ID" \
    "ud07LastAdminProbe=$(date -u +%Y%m%dT%H%M%SZ)" \
  --output none
```

Aggiornare tag sulla VM:

```bash
# Aggiorna tag sulla VM.
az tag update \
  --resource-id "$VM_ID" \
  --operation Merge \
  --tags \
    "ud07AdminProbe=manual-1" \
    "ud07AdminRunId=$ADMIN_RUN_ID" \
    "ud07LastAdminProbe=$(date -u +%Y%m%dT%H%M%SZ)" \
  --output none
```

---

## 8. Generazione ripetuta di attività amministrativa

Ora ripetiamo l'operazione in modo controllato. Il ciclo aggiorna tre volte i tag sulle risorse core.

```bash
# Svuota il log locale della generazione amministrativa.
: > logs/ud07_admin_activity_manual.log
: > logs/ud07_admin_errors_manual.log
```

```bash
# Genera tre round di aggiornamento tag sulle risorse core.
for round in 1 2 3
 do
  echo "=== Round amministrativo $round ===" | tee -a logs/ud07_admin_activity_manual.log

  while read -r RESOURCE_ID
  do
    # Salta righe vuote, se presenti.
    [[ -z "$RESOURCE_ID" ]] && continue

    echo "Aggiorno tag su: $RESOURCE_ID" | tee -a logs/ud07_admin_activity_manual.log

    if az tag update \
      --resource-id "$RESOURCE_ID" \
      --operation Merge \
      --tags \
        "ud07AdminProbe=round-${round}" \
        "ud07AdminRunId=${ADMIN_RUN_ID}" \
        "ud07LastAdminProbe=$(date -u +%Y%m%dT%H%M%SZ)" \
      --output none 2>> logs/ud07_admin_errors_manual.log
    then
      echo "OK: $RESOURCE_ID" | tee -a logs/ud07_admin_activity_manual.log
    else
      echo "ERRORE: $RESOURCE_ID" | tee -a logs/ud07_admin_errors_manual.log
    fi

    sleep 3
  done < logs/ud07_admin_resource_ids_core.txt

  sleep 10
 done
```

---

## 9. Verifica dal Portale dopo attività amministrativa

Dal Portale Azure aprire:

```text
Resource groups
→ <RG_NAME>
→ Activity log
→ Timespan: Last hour
```

Cercare eventi recenti relativi a:

```text
Microsoft.Resources/tags/write
operazioni di update/write sulla risorsa
modifiche ai tag
```

Poi aprire le singole risorse:

```text
Storage Account → Tags
App Service → Tags
Virtual Machine → Tags
```

Tag attesi:

```text
ud07AdminProbe
ud07AdminRunId
ud07LastAdminProbe
```

Domanda docente:

```text
Il fatto che i tag siano cambiati prova che l'applicazione ha ricevuto traffico?
```

Risposta attesa:

```text
No. Prova solo che è avvenuta un'operazione amministrativa sulla risorsa.
```

---

## 10. Raccolta Activity Log da CLI

Attendere un minuto:

```bash
# Attende la propagazione degli eventi in Activity Log.
sleep 60
```

Visualizzare eventi recenti:

```bash
# Mostra eventi recenti del Resource Group in forma tabellare.
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 30 \
  --query "[].{Time:eventTimestamp,Operation:operationName.localizedValue,Status:status.localizedValue,Caller:caller,Resource:resourceId}" \
  --output table
```

Salvare evidenze:

```bash
# Salva Activity Log in JSON.
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 80 \
  --output json > evidence/ud07_admin_activity_log_after_manual_tag_updates.json
```

```bash
# Salva Activity Log in formato tabellare testuale.
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 30 \
  --query "[].{Time:eventTimestamp,Operation:operationName.localizedValue,Status:status.localizedValue,Caller:caller,Resource:resourceId}" \
  --output table > evidence/ud07_admin_activity_log_after_manual_tag_updates_table.txt
```

Salvare tag finali:

```bash
# Salva i tag finali delle risorse principali.
az resource list \
  --resource-group "$RG_NAME" \
  --query "[?name=='$STORAGE_NAME' || name=='$APP_NAME' || name=='$VM_NAME'].{Name:name,Type:type,Tags:tags}" \
  --output json > evidence/ud07_admin_resource_tags_after_manual_updates.json
```

---

# PARTE B - Generazione di traffico applicativo e workload

Questa parte genera segnali sul **workload**. L'effetto atteso è:

```text
App Service: richieste HTTP e metrica Requests;
Storage Account: operazioni blob e metrica Transactions;
VM: eventuale carico CPU, se la VM è running e se RunCommand funziona.
```

---

## 11. Baseline prima del traffico applicativo

Prima di generare traffico, osservare la situazione iniziale.

### App Service, metrica Requests

```bash
# Salva la baseline della metrica Requests sull'App Service.
az monitor metrics list \
  --resource "$APP_ID" \
  --metric "Requests" \
  --interval PT1M \
  --aggregation Total \
  --output json > evidence/ud07_appservice_requests_baseline_before_manual_traffic.json
```

### Storage Account, metrica Transactions

```bash
# Salva la baseline della metrica Transactions sullo Storage Account.
az monitor metrics list \
  --resource "$STORAGE_ID" \
  --metric "Transactions" \
  --interval PT1M \
  --aggregation Total \
  --output json > evidence/ud07_storage_transactions_baseline_before_manual_traffic.json
```

### VM, metrica Percentage CPU

```bash
# Salva la baseline della CPU VM, se VM_ID è valorizzato.
az monitor metrics list \
  --resource "$VM_ID" \
  --metric "Percentage CPU" \
  --interval PT1M \
  --aggregation Average Maximum \
  --output json > evidence/ud07_vm_cpu_baseline_before_manual_workload.json
```

Dal Portale osservare:

```text
App Service → Metrics → Requests → Total
Storage Account → Metrics → Transactions → Total
VM → Metrics → Percentage CPU → Average / Maximum
```

Domanda docente:

```text
Se prima del test vediamo pochi dati, possiamo dire che la risorsa è guasta?
```

Risposta attesa:

```text
No. Può semplicemente non esserci stato traffico nel periodo osservato.
```

---

## 12. Generazione traffico HTTP su App Service

Recuperare hostname pubblico:

```bash
# Recupera l'hostname pubblico dell'App Service.
export APP_HOST="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query defaultHostName \
  --output tsv)"
```

Verificare:

```bash
# Mostra l'URL usato per generare traffico HTTP.
printf 'APP_HOST=%s\n' "$APP_HOST"
printf 'URL=https://%s/\n' "$APP_HOST"
```

Eseguire una richiesta singola:

```bash
# Prima richiesta di prova verso la home page.
curl -s -o /dev/null \
  -w "time=%{time_total}s status=%{http_code} url=%{url_effective}\n" \
  "https://$APP_HOST/"
```

Preparare il file CSV locale:

```bash
# Prepara il CSV locale con le richieste HTTP generate.
printf "timestamp,kind,url,http_status,time_total_seconds\n" > logs/ud07_appservice_http_traffic_manual.csv
```

Generare richieste verso la home page:

```bash
# Genera richieste HTTP verso la home page dell'App Service.
for i in $(seq 1 40)
 do
  URL="https://$APP_HOST/"
  RESULT="$(curl -sS -o /dev/null -w "%{http_code},%{time_total}" --max-time 10 "$URL" || printf "000,0")"

  printf "%s,home,%s,%s\n" \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    "$URL" \
    "$RESULT" >> logs/ud07_appservice_http_traffic_manual.csv

  sleep 1
 done
```

Generare richieste verso URL inesistenti:

```bash
# Genera richieste su URL inesistenti.
# Servono a produrre eventuali risposte 404 osservabili nelle metriche HTTP.
for i in $(seq 1 10)
 do
  URL="https://$APP_HOST/ud07-not-found-$i"
  RESULT="$(curl -sS -o /dev/null -w "%{http_code},%{time_total}" --max-time 10 "$URL" || printf "000,0")"

  printf "%s,not_found,%s,%s\n" \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    "$URL" \
    "$RESULT" >> logs/ud07_appservice_http_traffic_manual.csv

  sleep 1
 done
```

Verificare il CSV:

```bash
# Mostra le ultime richieste registrate localmente.
tail -10 logs/ud07_appservice_http_traffic_manual.csv
```

Domanda docente:

```text
Quale metrica ci aspettiamo di vedere crescere dopo queste richieste?
```

Risposta attesa:

```text
Requests sull'App Service.
```

---

## 13. Generazione traffico Storage Blob

Recuperare una key dello Storage Account:

```bash
# Recupera una key dello Storage Account.
# In laboratorio è una scelta pratica. In produzione è preferibile usare RBAC e identità gestite.
export STORAGE_KEY="$(az storage account keys list \
  --account-name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query "[0].value" \
  --output tsv)"
```

Definire il container:

```bash
# Container dedicato alla prova UD07.
export CONTAINER_NAME="ud07-app-traffic"
```

Creare il container:

```bash
# Crea il container, se non esiste già.
az storage container create \
  --account-name "$STORAGE_NAME" \
  --account-key "$STORAGE_KEY" \
  --name "$CONTAINER_NAME" \
  --output table
```

Preparare il CSV locale:

```bash
# Prepara il CSV locale con le operazioni Blob generate.
printf "timestamp,operation,blob_name,result\n" > logs/ud07_storage_blob_traffic_manual.csv
```

Eseguire una singola operazione completa:

```bash
# Crea un file locale di prova.
echo "UD07 storage manual probe - $(date -u)" > tmp/ud07_blob_single.txt
```

```bash
# Upload del file nel container.
az storage blob upload \
  --account-name "$STORAGE_NAME" \
  --account-key "$STORAGE_KEY" \
  --container-name "$CONTAINER_NAME" \
  --name "ud07/blob-single.txt" \
  --file tmp/ud07_blob_single.txt \
  --overwrite true \
  --output table
```

```bash
# Lista dei blob con prefisso ud07/.
az storage blob list \
  --account-name "$STORAGE_NAME" \
  --account-key "$STORAGE_KEY" \
  --container-name "$CONTAINER_NAME" \
  --prefix "ud07/" \
  --output table
```

```bash
# Download del blob.
az storage blob download \
  --account-name "$STORAGE_NAME" \
  --account-key "$STORAGE_KEY" \
  --container-name "$CONTAINER_NAME" \
  --name "ud07/blob-single.txt" \
  --file tmp/ud07_blob_single_downloaded.txt \
  --overwrite true \
  --output table
```

```bash
# Eliminazione del blob.
az storage blob delete \
  --account-name "$STORAGE_NAME" \
  --account-key "$STORAGE_KEY" \
  --container-name "$CONTAINER_NAME" \
  --name "ud07/blob-single.txt" \
  --output table
```

Ora generare traffico ripetuto:

```bash
# Genera upload, list, download e delete ripetuti.
for i in $(seq 1 20)
 do
  LOCAL_FILE="tmp/ud07_blob_${i}.txt"
  DOWNLOADED_FILE="tmp/ud07_blob_${i}_downloaded.txt"
  BLOB_NAME="ud07/blob-${i}.txt"

  printf "UD07 storage workload probe %s - %s\n" "$i" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$LOCAL_FILE"

  if az storage blob upload \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --container-name "$CONTAINER_NAME" \
    --name "$BLOB_NAME" \
    --file "$LOCAL_FILE" \
    --overwrite true \
    --output none
  then
    printf "%s,upload,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> logs/ud07_storage_blob_traffic_manual.csv
  else
    printf "%s,upload,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> logs/ud07_storage_blob_traffic_manual.csv
  fi

  if az storage blob list \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --container-name "$CONTAINER_NAME" \
    --prefix "ud07/" \
    --output none
  then
    printf "%s,list,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "ud07/" >> logs/ud07_storage_blob_traffic_manual.csv
  else
    printf "%s,list,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "ud07/" >> logs/ud07_storage_blob_traffic_manual.csv
  fi

  if az storage blob download \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --container-name "$CONTAINER_NAME" \
    --name "$BLOB_NAME" \
    --file "$DOWNLOADED_FILE" \
    --overwrite true \
    --output none
  then
    printf "%s,download,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> logs/ud07_storage_blob_traffic_manual.csv
  else
    printf "%s,download,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> logs/ud07_storage_blob_traffic_manual.csv
  fi

  if az storage blob delete \
    --account-name "$STORAGE_NAME" \
    --account-key "$STORAGE_KEY" \
    --container-name "$CONTAINER_NAME" \
    --name "$BLOB_NAME" \
    --output none
  then
    printf "%s,delete,%s,ok\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> logs/ud07_storage_blob_traffic_manual.csv
  else
    printf "%s,delete,%s,error\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$BLOB_NAME" >> logs/ud07_storage_blob_traffic_manual.csv
  fi

  sleep 1
 done
```

Verificare il CSV:

```bash
# Mostra le ultime operazioni Storage registrate localmente.
tail -12 logs/ud07_storage_blob_traffic_manual.csv
```

Domanda docente:

```text
Quale metrica ci aspettiamo di vedere crescere dopo queste operazioni?
```

Risposta attesa:

```text
Transactions sullo Storage Account.
```

---

## 14. Generazione workload VM, opzionale

Questa parte è opzionale. Va eseguita solo se la VM è running e se il docente vuole mostrare la metrica CPU.

Verificare lo stato VM con Azure Resource Manager REST:

```bash
# Versione API usata per leggere l'instance view della VM.
export COMPUTE_API_VERSION="2025-04-01"
```

```bash
# Legge lo stato operativo della VM.
az rest \
  --method get \
  --url "https://management.azure.com${VM_ID}/instanceView?api-version=${COMPUTE_API_VERSION}" \
  --query "statuses[].{Code:code,Status:displayStatus}" \
  --output table
```

Salvare lo stato:

```bash
# Salva l'instance view della VM.
az rest \
  --method get \
  --url "https://management.azure.com${VM_ID}/instanceView?api-version=${COMPUTE_API_VERSION}" \
  --output json > evidence/ud07_vm_instance_view_before_manual_workload.json
```

Estrarre il PowerState:

```bash
# Estrae il PowerState della VM.
export VM_POWER_STATE="$(az rest \
  --method get \
  --url "https://management.azure.com${VM_ID}/instanceView?api-version=${COMPUTE_API_VERSION}" \
  --query "statuses[?starts_with(code, 'PowerState/')].code | [0]" \
  --output tsv)"

printf 'VM_POWER_STATE=%s\n' "$VM_POWER_STATE"
```

Se il valore è:

```text
PowerState/running
```

si può generare un piccolo carico CPU:

```bash
# Genera un piccolo carico CPU nella VM per circa 20 secondi.
# Richiede che la VM sia running e che RunCommand sia disponibile.
az vm run-command invoke \
  --resource-group "$RG_NAME" \
  --name "$VM_NAME" \
  --command-id RunShellScript \
  --scripts "echo 'UD07 workload probe - ' \$(date -u) | sudo tee -a /var/log/ud07-workload-probe.log; timeout 20s bash -c 'while true; do :; done'" \
  --output json > evidence/ud07_vm_workload_runcommand_manual.json
```

Se la VM non è running o il comando fallisce, annotare nel report:

```text
La parte VM workload non è stata eseguita.
La VM non era running oppure RunCommand non era disponibile.
```

---

## 15. Attesa propagazione metriche

Azure Monitor non mostra sempre i dati immediatamente. Attendere qualche minuto.

```bash
# Attende la propagazione delle metriche.
echo "Attendo 3 minuti per la propagazione delle metriche Azure Monitor..."
sleep 180
```

---

## 16. Raccolta metriche dopo traffico

### App Service, Requests

```bash
# Mostra la metrica Requests dopo il traffico HTTP.
az monitor metrics list \
  --resource "$APP_ID" \
  --metric "Requests" \
  --interval PT1M \
  --aggregation Total \
  --output table
```

```bash
# Salva la metrica Requests dopo il traffico HTTP.
az monitor metrics list \
  --resource "$APP_ID" \
  --metric "Requests" \
  --interval PT1M \
  --aggregation Total \
  --output json > evidence/ud07_appservice_requests_after_manual_application_traffic.json
```

### Storage Account, Transactions

```bash
# Mostra la metrica Transactions dopo le operazioni Blob.
az monitor metrics list \
  --resource "$STORAGE_ID" \
  --metric "Transactions" \
  --interval PT1M \
  --aggregation Total \
  --output table
```

```bash
# Salva la metrica Transactions dopo le operazioni Blob.
az monitor metrics list \
  --resource "$STORAGE_ID" \
  --metric "Transactions" \
  --interval PT1M \
  --aggregation Total \
  --output json > evidence/ud07_storage_transactions_after_manual_application_traffic.json
```

### VM, Percentage CPU

```bash
# Mostra la metrica Percentage CPU dopo il workload VM, se eseguito.
az monitor metrics list \
  --resource "$VM_ID" \
  --metric "Percentage CPU" \
  --interval PT1M \
  --aggregation Average Maximum \
  --output table
```

```bash
# Salva la metrica Percentage CPU dopo il workload VM, se applicabile.
az monitor metrics list \
  --resource "$VM_ID" \
  --metric "Percentage CPU" \
  --interval PT1M \
  --aggregation Average Maximum \
  --output json > evidence/ud07_vm_cpu_after_manual_workload_probe.json
```

---

## 17. Verifica dal Portale dopo traffico applicativo

Dal Portale Azure osservare:

```text
App Service
→ Metrics
→ Requests
→ Aggregation: Total
→ Time range: Last hour
```

```text
Storage Account
→ Metrics
→ Transactions
→ Aggregation: Total
→ Time range: Last hour
```

```text
Virtual Machine
→ Metrics
→ Percentage CPU
→ Aggregation: Average / Maximum
→ Time range: Last hour
```

Domanda docente:

```text
Che differenza c'è tra ciò che abbiamo visto dopo l'aggiornamento tag e ciò che vediamo dopo il traffico applicativo?
```

Risposta attesa:

```text
L'aggiornamento tag produce Activity Log, cioè eventi amministrativi.
Il traffico HTTP e le operazioni Blob producono metriche operative come Requests e Transactions.
```

---

## 18. Evidenze finali prodotte

Verificare i file locali:

```bash
# Elenca le evidenze e i log prodotti.
find logs evidence -maxdepth 1 -type f | sort
```

File attesi principali:

```text
logs/ud07_admin_activity_manual.log
logs/ud07_admin_errors_manual.log
logs/ud07_admin_resource_ids_core.txt
logs/ud07_appservice_http_traffic_manual.csv
logs/ud07_storage_blob_traffic_manual.csv

evidence/ud07_resource_inventory_before_generation.json
evidence/ud07_core_resource_ids.txt
evidence/ud07_admin_activity_log_after_manual_tag_updates.json
evidence/ud07_admin_activity_log_after_manual_tag_updates_table.txt
evidence/ud07_admin_resource_tags_after_manual_updates.json
evidence/ud07_appservice_requests_baseline_before_manual_traffic.json
evidence/ud07_storage_transactions_baseline_before_manual_traffic.json
evidence/ud07_vm_cpu_baseline_before_manual_workload.json
evidence/ud07_appservice_requests_after_manual_application_traffic.json
evidence/ud07_storage_transactions_after_manual_application_traffic.json
evidence/ud07_vm_cpu_after_manual_workload_probe.json
```

---

## 19. Tabella di interpretazione

Compilare nel report:

| Attività | Tipo segnale | Dove si osserva | Evidenza locale | Interpretazione |
|---|---|---|---|---|
| Aggiornamento tag | Amministrativo | Activity Log | `evidence/ud07_admin_activity_log_after_manual_tag_updates.json` | Mostra operazioni sul piano di controllo Azure |
| Richieste HTTP App Service | Applicativo/workload | Metrics, Requests | `evidence/ud07_appservice_requests_after_manual_application_traffic.json` | Mostra traffico verso l'applicazione |
| Operazioni Blob | Workload storage | Metrics, Transactions | `evidence/ud07_storage_transactions_after_manual_application_traffic.json` | Mostra uso dello Storage Account |
| Carico CPU VM | Workload infrastrutturale | Metrics, Percentage CPU | `evidence/ud07_vm_cpu_after_manual_workload_probe.json` | Mostra utilizzo compute, se la VM era running |

---

## 20. Domande finali docente

### Domanda 1

```text
Quale attività genera Activity Log?
```

Risposta attesa:

```text
L'aggiornamento tag sulle risorse.
```

### Domanda 2

```text
Quale attività genera Requests sull'App Service?
```

Risposta attesa:

```text
Le richieste HTTP eseguite con curl verso l'hostname dell'App Service.
```

### Domanda 3

```text
Quale attività genera Transactions sullo Storage Account?
```

Risposta attesa:

```text
Le operazioni Blob: upload, list, download e delete.
```

### Domanda 4

```text
Perché facciamo baseline prima e verifica dopo?
```

Risposta attesa:

```text
Per confrontare lo stato iniziale con lo stato successivo alla generazione controllata del segnale.
```

### Domanda 5

```text
Se dopo il traffico non vedo subito la metrica aggiornata, quale ipotesi faccio?
```

Risposta attesa:

```text
Azure Monitor può avere latenza. Aspetto alcuni minuti, verifico time range, aggregazione e risorsa selezionata.
```

---

## 21. Stato Git finale

```bash
# Controlla file nuovi o modificati.
git status
```

Aggiungere i file prodotti:

```bash
# Aggiunge evidenze, log e report al commit.
git add docs evidence logs
```

Commit:

```bash
# Crea un commit descrittivo.
git commit -m "UD07 generazione controllata segnali osservabili"
```

Push:

```bash
# Pubblica il lavoro sul repository remoto.
git push
```

---

## 22. Sintesi didattica

```text
UD06: abbiamo imparato a riconoscere i segnali disponibili.
UD07: generiamo segnali controllati e li interpretiamo prima/dopo.
```

Distinzione fondamentale:

```text
Aggiornare tag produce segnali amministrativi.
Chiamare l'App Service produce traffico applicativo.
Usare Blob Storage produce transazioni storage.
Generare carico nella VM produce workload infrastrutturale.
```

La conclusione da portare a casa è questa:

```text
Non basta vedere un grafico o un log.
Bisogna sapere quale attività lo ha prodotto, dove osservarlo e quale domanda diagnostica permette di rispondere.
```

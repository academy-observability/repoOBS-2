# 01 - Laboratorio guidato UD07 v4

# Azure Monitor, metriche, Diagnostic Settings e segnali generati

## 1. Obiettivo del laboratorio

In questo laboratorio guidato analizziamo metriche Azure Monitor su risorse già create in UD05 e già osservate in UD06.

La novità è che non ci limitiamo a guardare grafici già presenti: generiamo segnali controllati e confrontiamo la situazione prima/dopo.

Alla fine avremo:

```text
letto metriche dal Portale Azure;
esportato metric definitions e metric values da CLI;
generato attività amministrativa e osservato Activity Log;
generato traffico applicativo/workload e osservato metriche;
verificato categorie diagnostiche e Diagnostic Settings;
compilato un report tecnico con evidenze.
```

Non creiamo nuove risorse Azure. Usiamo quelle già disponibili.

## 2. Prerequisiti

Verificare di avere:

```text
accesso al Portale Azure;
Azure CLI disponibile in WSL o terminale locale;
login Azure già effettuato;
subscription corretta selezionata;
Resource Group UD05 ancora presente;
Storage Account, App Service e VM, se disponibili;
repository locale aggiornato.
```

Se una risorsa non è presente, non improvvisare creazioni. Si salta la parte relativa o si usa una risorsa assegnata dal docente. Incredibile, ma non ogni problema si risolve creando un'altra risorsa da pagare.

## 3. Regola su WSL, terminale locale e Cloud Shell

I comandi che scrivono file in `docs/`, `evidence/`, `logs/` o `img/` devono essere eseguiti dal repository locale.

Usare:

```text
WSL o terminale locale = comandi, script, redirection su file locali.
Cloud Shell = verifiche rapide, output tabellari, screenshot, controlli dal Portale.
```

Prima di iniziare, entrare nella cartella UD07 del repository:

```bash
cd ~/corso_obs/obs-labs-2026-*/work/UD07
```

Adattare il percorso al proprio repository.

## 4. Preparazione cartelle

```bash
mkdir -p src config docs evidence logs img
```

Verificare:

```bash
find . -maxdepth 2 -type d | sort
```

## 5. Configurazione ambiente UD07

Copiare il file di esempio:

```bash
cp config/ud07.env.example config/ud07.env
```

Aprire `config/ud07.env` e inserire i valori del proprio laboratorio:

```bash
nano config/ud07.env
```

Esempio di valori:

```bash
SUB_ID="<id-subscription>"
RG_NAME="rg-obs-ud05-<codice>"
STORAGE_NAME="stobsud05<codice>01"
APP_NAME="app-obs-ud05-<codice>"
VM_NAME="vm01"
```

Caricare le variabili nel terminale corrente:

```bash
set -a
source config/ud07.env
set +a
```

Verificare:

```bash
printf 'SUB_ID=%s\n' "$SUB_ID"
printf 'RG_NAME=%s\n' "$RG_NAME"
printf 'STORAGE_NAME=%s\n' "$STORAGE_NAME"
printf 'APP_NAME=%s\n' "$APP_NAME"
printf 'VM_NAME=%s\n' "$VM_NAME"
```

Se una variabile non stampa nulla, è vuota. Prima si corregge quella, poi si accusa Azure. È un ordine sano delle cose.

## 6. Verifica Azure CLI e contesto

Eseguire:

```bash
chmod +x src/verifica_ud07.sh
./src/verifica_ud07.sh
```

Il comando produce:

```text
evidence/ud07_account_context.json
```

Verifica manuale equivalente:

```bash
az account set --subscription "$SUB_ID"

az account show \
  --query "{subscription:name,id:id,user:user.name}" \
  --output table
```

Domanda docente:

```text
La subscription mostrata dalla CLI è la stessa che usi nel Portale?
```

Risposta attesa:

```text
Sì, nome o ID subscription coincidono. Se non coincidono, devo impostare la subscription corretta.
```

## 7. Inventario rapido, senza rifare UD06

Qui facciamo solo un controllo rapido.

```bash
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{Name:name,Type:type,Location:location}" \
  --output table
```

Salvare evidenza:

```bash
az resource list \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud07_resource_inventory.json
```

Domanda docente:

```text
Questo è il cuore della UD07?
```

Risposta attesa:

```text
No. Serve solo a confermare quali risorse useremo. Il cuore della UD07 è leggere metriche e generare segnali controllati.
```

## 8. Recupero Resource ID delle risorse principali

```bash
export STORAGE_ID="$(az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv 2>/dev/null || true)"

# Recupera automaticamente la prima Web App presente nel Resource Group.
# Nel laboratorio UD07 ce n'è una sola.
export APP_NAME="$(az resource list \
  --resource-group "$RG_NAME" \
  --resource-type "Microsoft.Web/sites" \
  --query "[0].name" \
  --output tsv)"

# Recupera il Resource ID della Web App.
export APP_ID="$(az resource list \
  --resource-group "$RG_NAME" \
  --resource-type "Microsoft.Web/sites" \
  --query "[0].id" \
  --output tsv)"


export VM_ID="$(az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv 2>/dev/null || true)"

printf 'STORAGE_ID=%s\nAPP_ID=%s\nVM_ID=%s\n' "$STORAGE_ID" "$APP_ID" "$VM_ID" | tee evidence/ud07_core_resource_ids.txt
```

Se `VM_ID` è vuoto, la VM non è stata trovata nella subscription o nel Resource Group indicato. Non è una tragedia greca: si salta la parte VM.

## 9. Baseline dal Portale Azure

Prima di generare traffico, osservare la situazione iniziale.

### App Service

Percorso:

```text
App Service
→ app-obs-ud05-<codice>
→ Monitoring
→ Metrics
→ Metric: Requests
→ Aggregation: Count
→ Time range: Last hour
```

Screenshot consigliato:

```text
img/ud07_baseline_appservice_requests.png
```

### Storage Account

Percorso:

```text
Storage Account
→ stobsud05...
→ Monitoring
→ Metrics
→ Metric: Transactions
→ Aggregation: Sum
→ Time range: Last hour
```

Screenshot consigliato:

```text
img/ud07_baseline_storage_transactions.png
```

### VM, se presente

Percorso:

```text
Virtual Machine
→ vm01
→ Monitoring
→ Metrics
→ Metric: Percentage CPU
→ Aggregation: Average / Maximum
→ Time range: Last hour
```

Screenshot consigliato:

```text
img/ud07_baseline_vm_cpu.png
```

Domanda docente:

```text
Se prima del test vedo pochi dati o nessun dato, posso dire che la risorsa è guasta?
```

Risposta attesa:

```text
No. Potrebbe semplicemente non esserci stato traffico o workload nel periodo osservato.
```

## 10. Baseline da CLI

### Definizioni metriche App Service

```bash
bash src/az_metric_definitions.sh "$APP_ID" evidence/ud07_appservice_metric_definitions.json
```

### Valori iniziali Requests

```bash
bash src/az_metrics_snapshot.sh "$APP_ID" "Requests" PT1M Total evidence/ud07_appservice_requests_baseline.json
```

### Definizioni metriche Storage

```bash
bash src/az_metric_definitions.sh "$STORAGE_ID" evidence/ud07_storage_metric_definitions.json
```

### Valori iniziali Transactions

```bash
bash src/az_metrics_snapshot.sh "$STORAGE_ID" "Transactions" PT1M Total evidence/ud07_storage_transactions_baseline.json
```

### VM CPU, se VM_ID è valorizzato

```bash
if [[ -n "${VM_ID:-}" ]]; then
  bash src/az_metrics_snapshot.sh "$VM_ID" "Percentage CPU" PT1M "Average Maximum" evidence/ud07_vm_cpu_baseline.json
fi
```

## 11. Generazione attività amministrativa passo dopo passo

In questa versione non usiamo lo script automatico. I partecipanti eseguono i comandi dalla guida operativa:

```text
04_OBS_UD07_GENERAZIONE_CONTROLLATA_SEGNALI_Passo_Passo.md
```

Usare in particolare le sezioni:

```text
PARTE A - Generazione di attività amministrativa
6. Creazione lista risorse core
7. Primo aggiornamento tag, esecuzione esplicita
8. Generazione ripetuta di attività amministrativa
9. Verifica dal Portale dopo attività amministrativa
10. Raccolta Activity Log da CLI
```

Output principali attesi:

```text
logs/ud07_admin_activity_manual.log
logs/ud07_admin_errors_manual.log
logs/ud07_admin_resource_ids_core.txt
evidence/ud07_admin_activity_log_after_manual_tag_updates.json
evidence/ud07_admin_activity_log_after_manual_tag_updates_table.txt
evidence/ud07_admin_resource_tags_after_manual_updates.json
```

### Dal Portale Azure

Aprire:

```text
Resource groups
→ <RG_NAME>
→ Activity log
→ Timespan: Last hour
```

Poi aprire le singole risorse:

```text
Storage Account → Activity log / Tags
App Service → Activity log / Tags
Virtual Machine → Activity log / Tags
```

Domanda docente:

```text
Che tipo di segnale abbiamo generato?
```

Risposta attesa:

```text
Abbiamo generato eventi amministrativi del piano di controllo Azure, visibili in Activity Log.
```

Domanda docente:

```text
Questo prova che l'applicazione riceve traffico?
```

Risposta attesa:

```text
No. Aggiornare tag non equivale a chiamare l'applicazione. È attività amministrativa.
```

## 12. Generazione traffico applicativo e workload passo dopo passo

In questa versione non usiamo lo script automatico. I partecipanti eseguono i comandi dalla guida operativa:

```text
04_OBS_UD07_GENERAZIONE_CONTROLLATA_SEGNALI_Passo_Passo.md
```

Usare in particolare le sezioni:

```text
PARTE B - Generazione di traffico applicativo e workload
11. Baseline prima del traffico applicativo
12. Generazione traffico HTTP su App Service
13. Generazione traffico Storage Blob
14. Generazione workload VM, opzionale
15. Attesa propagazione metriche
16. Raccolta metriche dopo traffico
```

Output principali attesi:

```text
logs/ud07_appservice_http_traffic_manual.csv
logs/ud07_storage_blob_traffic_manual.csv
evidence/ud07_appservice_requests_after_manual_application_traffic.json
evidence/ud07_storage_transactions_after_manual_application_traffic.json
evidence/ud07_vm_cpu_after_manual_workload_probe.json, se VM applicabile
```

Azure Monitor può richiedere alcuni minuti prima di mostrare le metriche aggiornate. Il laboratorio prevede quindi una breve attesa prima della raccolta finale.

## 13. Osservazione dopo traffico dal Portale

### App Service

```text
App Service
→ Metrics
→ Requests
→ Aggregation: Total
→ Time range: Last hour
```

Domanda docente:

```text
Cosa ti aspetti dopo lo script applicativo?
```

Risposta attesa:

```text
Mi aspetto un aumento o comunque la presenza di punti nella metrica Requests.
```

### Storage Account

```text
Storage Account
→ Metrics
→ Transactions
→ Aggregation: Total
→ Time range: Last hour
```

Domanda docente:

```text
Perché Transactions dovrebbe cambiare?
```

Risposta attesa:

```text
Perché lo script ha eseguito operazioni blob: upload, list, download e delete.
```

### VM, se usata

```text
Virtual Machine
→ Metrics
→ Percentage CPU
→ Aggregation: Average e Maximum
```

Domanda docente:

```text
Perché confrontare Average e Maximum sulla CPU?
```

Risposta attesa:

```text
Average mostra il carico medio. Maximum aiuta a vedere eventuali picchi brevi.
```

## 14. Verifica Diagnostic Settings

Scegliere una risorsa, per esempio App Service:

```bash
bash src/az_diagnostic_settings_inventory.sh "$APP_ID" evidence/ud07_appservice_diagnostic_settings.json evidence/ud07_appservice_diagnostic_categories.json
```

Dal Portale:

```text
App Service
→ Monitoring
→ Diagnostic settings
```

Domanda docente:

```text
In UD07 dobbiamo per forza creare un Diagnostic Setting?
```

Risposta attesa:

```text
No. In UD07 possiamo verificare categorie e impostazioni esistenti. La raccolta verso Log Analytics viene approfondita nelle UD successive.
```

Se la blade del Portale non si carica o compare un errore su `Microsoft.Insights`, documentare lo screenshot e usare la CLI come evidenza alternativa.

## 15. Creazione report guidato

Copiare il template:

```bash
cp docs/template_report_ud07.md docs/report_ud07_metriche_segnali_generati.md
```

Compilare almeno queste sezioni:

```text
risorse osservate;
baseline prima dei test;
segnale amministrativo generato;
segnale applicativo generato;
metriche osservate;
confronto prima/dopo;
evidenze prodotte;
limiti e anomalie;
conclusione tecnica.
```

## 16. Verifica finale dei file

```bash
find docs evidence logs img -maxdepth 2 -type f | sort
```

Controllare Git:

```bash
git status
```

Commit suggerito:

```bash
git add docs evidence logs img config src

git commit -m "Completamento UD07 metriche e segnali generati"
```

Se il docente usa repository individuali con commit obbligatorio, eseguire anche:

```bash
git push
```

## 17. Criteri di completamento

Il laboratorio guidato è completato quando il partecipante sa mostrare:

```text
baseline dal Portale;
output CLI in evidence/;
Activity Log generato dallo script amministrativo;
metriche generate dallo script applicativo;
differenza tra segnale amministrativo e applicativo;
report con interpretazione prima/dopo;
git status coerente.
```

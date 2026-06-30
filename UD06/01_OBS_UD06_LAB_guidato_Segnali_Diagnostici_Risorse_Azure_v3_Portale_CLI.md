# OBS_UD06 - Laboratorio guidato
# Segnali diagnostici delle risorse Azure già create

## Versione v4 - Portale Azure + CLI

## 1. Obiettivo del laboratorio

In questo laboratorio analizziamo le risorse create o osservate in UD05.

Non creiamo nuove risorse. Lavoriamo su:

```text
Resource Group esistente
Storage Account / static website, se presente
App Service, se presente
VM Linux, se presente
eventuali risorse collegate
```

L'obiettivo è riconoscere e salvare i principali segnali diagnostici:

```text
inventario risorse
stato risorse
Activity Log
metriche disponibili
valori metrici recenti
categorie diagnostiche
Diagnostic Settings esistenti
evidenze e interpretazione
```

La versione v4 introduce una regola didattica esplicita:

```text
prima osserviamo il segnale dal Portale Azure;
poi usiamo la CLI per produrre un'evidenza salvabile nel repository.
```

Il Portale aiuta a orientarsi e a capire dove si trovano i segnali. La CLI aiuta a salvare output ripetibili e versionabili. Usare solo una delle due viste riduce la comprensione: il Portale senza evidenze è fragile, la CLI senza orientamento visivo diventa un elenco di comandi.

---

## 2. Prerequisiti

Prima di iniziare dobbiamo avere:

```text
[ ] UD05 completata
[ ] accesso al Portale Azure
[ ] Azure CLI funzionante in WSL o terminale locale
[ ] subscription corretta selezionata
[ ] Resource Group UD05 ancora presente oppure risorse demo docente disponibili
[ ] repository locale della UD06 disponibile
```


---

## 3. Nota operativa su WSL, terminale locale e Cloud Shell

In questa UD molti comandi salvano output JSON dentro `evidence/`.

Questi comandi devono essere eseguiti **dal repository locale**, normalmente in WSL o in un terminale locale con Azure CLI installata e autenticata.

Azure Cloud Shell può essere usata per verifiche rapide, ma non va considerata equivalente al repository locale. Se in Cloud Shell eseguiamo un comando come:

```bash
# In Cloud Shell questo file viene creato nell'ambiente remoto di Cloud Shell,
# non nel repository locale del partecipante.
az account show --output json > evidence/ud06_account_context.json
```

il file viene creato nell'ambiente remoto di Cloud Shell, non nella cartella `evidence/` del repository del partecipante.

Regola della UD06:

```text
Comandi con > evidence/...  -> WSL o terminale locale dentro il repository.
Cloud Shell                  -> output da copiare nel report o screenshot, senza redirection verso evidence/.
Portale Azure                -> orientamento visuale, screenshot e confronto con la CLI.
```

---

## 4. Preparazione cartelle

Posizionarsi nella directory della UD06.

Creare le cartelle:

```bash
# Crea le cartelle locali usate per report, evidenze e log.
mkdir -p docs evidence logs
```

Creare il file report:

```bash
# Crea il file Markdown che compileremo durante il laboratorio.
touch docs/report_ud06_segnali_diagnostici_azure.md
```

Verificare:

```bash
# Mostra la cartella corrente e l'albero minimo dei file locali.
pwd
find docs evidence logs -maxdepth 2 -type f | sort
```

---

## 5. Variabili di lavoro

Impostare le variabili in base ai nomi usati in UD05.

Esempio:

```bash
# Nome del Resource Group creato o usato nella UD05.
export RG_NAME="rg-obs-ud05-mrossi"

# Nome dello Storage Account, se creato in UD05.
export STORAGE_NAME="stobsud05mrossi01"

# Nome dell'App Service, se creato in UD05.
export APP_NAME="app-obs-ud05-mrossi"

# Nome della VM, se creata o analizzata in UD05.
export VM_NAME="vm-obs-ud05-mrossi"
```

Se una risorsa non è stata creata in UD05, lasciare vuota la relativa variabile:

```bash
# Esempio: nessuna VM disponibile.
export VM_NAME=""
```

Verificare:

```bash
# Stampa le variabili usate dal laboratorio.
printf 'RG_NAME=%s\n' "$RG_NAME"
printf 'STORAGE_NAME=%s\n' "$STORAGE_NAME"
printf 'APP_NAME=%s\n' "$APP_NAME"
printf 'VM_NAME=%s\n' "$VM_NAME"
```

---

# Parte A - Contesto Azure

## 6. Verifica contesto Azure

### 6.1 Vista da Portale Azure

Dal Portale Azure:

```text
https://portal.azure.com
```

Controllare:

```text
account in alto a destra
directory o tenant corrente
subscription usata nel laboratorio
```

Percorsi utili nel Portale:

```text
Home -> Subscriptions
oppure
barra di ricerca -> Subscriptions
```

Osservare:

```text
nome subscription
stato subscription
tenant associato
ruolo o permessi visibili, se disponibili
```

Evidenza consigliata:

```text
evidence/ud06_portal_subscription_context.png
```

### 6.2 Vista da CLI

Salvare il contesto Azure corrente dal repository locale:

```bash
# Eseguire da WSL o terminale locale dentro la cartella della UD06.
# Il file JSON viene salvato nella cartella evidence del repository.
az account show --output json > evidence/ud06_account_context.json
```

Leggere i campi principali:

```bash
# Vista sintetica del contesto Azure corrente.
az account show \
  --query "{name:name, id:id, tenantId:tenantId, user:user.name}" \
  --output table
```

Questa vista tabellare può essere eseguita anche in Cloud Shell, perché non scrive file locali. In quel caso copiare i valori principali nel report.

### 6.3 Confronto Portale / CLI

| Aspetto | Portale Azure | CLI |
|---|---|---|
| Orientamento iniziale | più leggibile | più sintetico |
| Evidenza versionabile | screenshot manuale | JSON salvato in `evidence/` |
| Ripetibilità | bassa | alta |
| Rischio errore | cambio tenant o subscription non notato | subscription errata se non verificata |

Nel report indicare:

```text
subscription usata
tenant
utente
data/ora verifica
modalità di verifica: Portale + CLI
```

---

# Parte B - Resource Group e inventario

## 7. Inventario Resource Group

### 7.1 Vista da Portale Azure

Dal Portale Azure:

```text
Resource groups
-> rg-obs-ud05-<codice>
```

Osservare nella pagina **Overview**:

```text
nome Resource Group
subscription
regione
numero di risorse
elenco risorse principali
tag applicati
```

Aprire anche la sezione **Resources**, se disponibile, e osservare:

```text
tipo risorsa
nome risorsa
località
collegamenti tra risorse, per esempio VM, disco, NIC, IP pubblico, rete
```

Evidenze consigliate:

```text
evidence/ud06_portal_rg_overview.png
evidence/ud06_portal_rg_resources.png
```

### 7.2 Vista da CLI

Verificare che il Resource Group esista:

```bash
# Eseguire da WSL o terminale locale dentro il repository.
# L'output viene salvato in evidence/.
az group show \
  --name "$RG_NAME" \
  --output json > evidence/ud06_rg_details.json
```

Salvare l'inventario:

```bash
# Salva l'elenco completo delle risorse contenute nel Resource Group.
az resource list \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_rg_inventory.json
```

Visualizzare una tabella sintetica:

```bash
# Mostra una vista compatta leggibile in aula.
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{name:name,type:type,location:location}" \
  --output table
```

### 7.3 Confronto Portale / CLI

| Domanda | Dove si vede meglio? | Nota |
|---|---|---|
| Quali risorse contiene il Resource Group? | Portale e CLI | il Portale è più visivo, la CLI è più esportabile |
| Quali risorse sono collegate alla VM? | Portale | la relazione è più intuitiva nella UI |
| Quante risorse sono presenti? | CLI | facile salvare e confrontare l'inventario |
| Ci sono risorse inattese? | entrambi | controllare nomi, tipi e tag |

Nel report rispondere:

```text
Quante risorse sono presenti?
Quali tipi di risorse troviamo?
Quali risorse sembrano collegate tra loro?
Ci sono risorse inattese?
Il Portale e la CLI mostrano informazioni coerenti?
```

---

# Parte C - Activity Log

## 8. Activity Log del Resource Group

L'Activity Log mostra operazioni amministrative. Non è il log applicativo della risorsa.

### 8.1 Vista da Portale Azure

Dal Portale Azure:

```text
Resource groups
-> rg-obs-ud05-<codice>
-> Activity log
```

Osservare:

```text
operazioni recenti
stato dell'operazione
utente o caller
timestamp
eventuali failure
eventuali modifiche su risorse o tag
```

Applicare, se necessario, un filtro temporale sulle ultime ore o sull'ultima giornata.

Evidenza consigliata:

```text
evidence/ud06_portal_activity_log.png
```

### 8.2 Vista da CLI

Salvare gli eventi recenti:

```bash
# Salva gli ultimi eventi amministrativi del Resource Group.
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 20 \
  --output json > evidence/ud06_activity_log.json
```

Vista sintetica:

```bash
# Mostra una tabella con timestamp, operazione, stato e caller.
az monitor activity-log list \
  --resource-group "$RG_NAME" \
  --max-events 10 \
  --query "[].{time:eventTimestamp,operation:operationName.value,status:status.value,caller:caller}" \
  --output table
```

### 8.3 Confronto Portale / CLI

| Aspetto | Portale Azure | CLI |
|---|---|---|
| Filtro visuale | comodo | possibile ma meno immediato |
| Lettura singolo evento | comoda | ricca ma più verbosa |
| Evidenza JSON | manuale | naturale |
| Uso nel report | screenshot + interpretazione | file JSON + tabella sintetica |

Nel report indicare:

```text
operazioni più recenti
eventuali failure
eventuali start/stop
eventuali modifiche tag/configurazione
quale evento sembra più rilevante e perché
```

---

# Parte D - Storage Account, se presente

## 9. Analisi Storage Account

Saltare questa sezione se `STORAGE_NAME` è vuota.

## 9.1 Dettagli e stato della risorsa

### Vista da Portale Azure

Dal Portale Azure:

```text
Resource groups
-> rg-obs-ud05-<codice>
-> Storage Account
-> Overview
```

Osservare:

```text
nome
Resource Group
regione
performance
replication
stato provisioning
endpoint disponibili
static website, se abilitato
```

Evidenza consigliata:

```text
evidence/ud06_portal_storage_overview.png
```

### Vista da CLI

Recuperare dettagli risorsa:

```bash
# Salva i dettagli dello Storage Account in JSON.
az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_storage_details.json
```

Estrarre Resource ID:

```bash
# Estrae il Resource ID, necessario per interrogare metriche e diagnostic settings.
export STORAGE_ID="$(az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

Verificare:

```bash
# Stampa il Resource ID ottenuto.
printf 'STORAGE_ID=%s\n' "$STORAGE_ID"
```

## 9.2 Metriche Storage

### Vista da Portale Azure

Dal Portale Azure:

```text
Storage Account
-> Monitoring
-> Metrics
```

Selezionare, se disponibile:

```text
Metric namespace: Account
Metric: Transactions
Aggregation: Sum o Count, secondo disponibilità
Time range: ultime 1 o 3 ore
```

Osservare:

```text
ci sono valori recenti?
la risorsa ha ricevuto traffico?
il grafico è vuoto?
il time range è adeguato?
```

Evidenza consigliata:

```text
evidence/ud06_portal_storage_metrics_transactions.png
```

### Vista da CLI

Metriche disponibili:

```bash
# Salva l'elenco delle metriche disponibili per lo Storage Account.
az monitor metrics list-definitions \
  --resource "$STORAGE_ID" \
  --output json > evidence/ud06_storage_metric_definitions.json
```

Vista sintetica:

```bash
# Mostra nome, unità e aggregazione primaria delle metriche disponibili.
az monitor metrics list-definitions \
  --resource "$STORAGE_ID" \
  --query "[].{name:name.value,unit:unit,primaryAggregation:primaryAggregationType}" \
  --output table
```

Valori metrici recenti, esempio `Transactions`:

```bash
# Salva valori recenti della metrica Transactions.
az monitor metrics list \
  --resource "$STORAGE_ID" \
  --metric Transactions \
  --interval PT5M \
  --output json > evidence/ud06_storage_metric_values.json
```

## 9.3 Diagnostic Settings Storage

### Vista da Portale Azure

Dal Portale Azure:

```text
Storage Account
-> Monitoring
-> Diagnostic settings
```

Osservare:

```text
sono presenti Diagnostic Settings?
quali categorie di log o metriche sono disponibili?
ci sono destinazioni configurate, per esempio Log Analytics?
```

Non creare o modificare Diagnostic Settings in UD06, salvo autorizzazione esplicita del docente.

Evidenza consigliata:

```text
evidence/ud06_portal_storage_diagnostic_settings.png
```

### Vista da CLI

Categorie diagnostiche disponibili:

```bash
# Salva le categorie diagnostiche disponibili per la risorsa.
az monitor diagnostic-settings categories list \
  --resource "$STORAGE_ID" \
  --output json > evidence/ud06_storage_diagnostic_categories.json
```

Diagnostic Settings esistenti:

```bash
# Salva l'elenco dei Diagnostic Settings già configurati.
az monitor diagnostic-settings list \
  --resource "$STORAGE_ID" \
  --output json > evidence/ud06_storage_diagnostic_settings.json
```

## 9.4 Interpretazione Storage

Nel report rispondere:

```text
Lo Storage Account ha metriche disponibili?
La metrica Transactions ha dati recenti?
Sono presenti Diagnostic Settings?
Quali categorie diagnostiche risultano disponibili?
Quale domanda diagnostica posso rispondere con questi segnali?
Il Portale e la CLI mostrano informazioni coerenti?
```

---

# Parte E - App Service, se presente

## 10. Analisi App Service

Saltare questa sezione se `APP_NAME` è vuota.

## 10.1 Dettagli e stato della Web App

### Vista da Portale Azure

Dal Portale Azure:

```text
Resource groups
-> rg-obs-ud05-<codice>
-> App Service
-> Overview
```

Osservare:

```text
nome
stato
Default domain
App Service Plan
runtime stack
regione
HTTPS only
```

Aprire il default domain in una nuova scheda, se disponibile, per verificare se la Web App risponde.

Evidenze consigliate:

```text
evidence/ud06_portal_appservice_overview.png
evidence/ud06_portal_appservice_default_domain.png
```

### Vista da CLI

Dettagli Web App:

```bash
# Salva i dettagli completi della Web App.
az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_appservice_details.json
```

Resource ID:

```bash
# Estrae il Resource ID della Web App.
export APP_ID="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

Stato sintetico:

```bash
# Mostra stato, hostname, tipo e impostazione HTTPS.
az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query "{name:name,state:state,host:defaultHostName,kind:kind,httpsOnly:httpsOnly}" \
  --output table
```

## 10.2 Metriche App Service

### Vista da Portale Azure

Dal Portale Azure:

```text
App Service
-> Monitoring
-> Metrics
```

Metriche utili da cercare, se disponibili:

```text
Requests
Average Response Time
Http 5xx
Http 4xx
CPU Time
Memory Working Set
```

Osservare:

```text
ci sono richieste recenti?
ci sono errori 4xx o 5xx?
il grafico è vuoto per assenza di traffico?
il time range è coerente con l'attività svolta?
```

Evidenza consigliata:

```text
evidence/ud06_portal_appservice_metrics_requests.png
```

### Vista da CLI

Metriche disponibili:

```bash
# Salva l'elenco delle metriche disponibili per la Web App.
az monitor metrics list-definitions \
  --resource "$APP_ID" \
  --output json > evidence/ud06_appservice_metric_definitions.json
```

Vista sintetica:

```bash
# Mostra una tabella delle metriche disponibili.
az monitor metrics list-definitions \
  --resource "$APP_ID" \
  --query "[].{name:name.value,unit:unit,aggregation:primaryAggregationType}" \
  --output table
```

Valori metrici recenti, esempio `Requests`:

```bash
# Salva valori recenti della metrica Requests.
az monitor metrics list \
  --resource "$APP_ID" \
  --metric Requests \
  --interval PT5M \
  --output json > evidence/ud06_appservice_metric_values.json
```

## 10.3 Diagnostic Settings App Service

### Vista da Portale Azure

Dal Portale Azure:

```text
App Service
-> Monitoring
-> Diagnostic settings
```

Osservare:

```text
sono presenti Diagnostic Settings?
quali categorie log sono disponibili?
le metriche possono essere inviate a una destinazione?
esiste una destinazione Log Analytics?
```

Non creare o modificare Diagnostic Settings in UD06, salvo autorizzazione esplicita del docente.

Evidenza consigliata:

```text
evidence/ud06_portal_appservice_diagnostic_settings.png
```

### Vista da CLI

Categorie diagnostiche:

```bash
# Salva le categorie diagnostiche disponibili per la Web App.
az monitor diagnostic-settings categories list \
  --resource "$APP_ID" \
  --output json > evidence/ud06_appservice_diagnostic_categories.json
```

Diagnostic Settings:

```bash
# Salva l'elenco dei Diagnostic Settings esistenti.
az monitor diagnostic-settings list \
  --resource "$APP_ID" \
  --output json > evidence/ud06_appservice_diagnostic_settings.json
```

## 10.4 Interpretazione App Service

Nel report rispondere:

```text
La Web App risulta Running?
Quale hostname espone?
Quali metriche sono disponibili?
Ci sono valori recenti per Requests?
Ci sono categorie diagnostiche disponibili?
Esiste già un Diagnostic Setting?
Il Portale e la CLI mostrano informazioni coerenti?
```

---

# Parte F - VM Linux, se presente

## 11. Analisi VM

Saltare questa sezione se `VM_NAME` è vuota.

## 11.1 Dettagli e stato operativo

### Vista da Portale Azure

Dal Portale Azure:

```text
Resource groups
-> rg-obs-ud05-<codice>
-> Virtual Machine
-> Overview
```

Osservare:

```text
stato della VM
size
sistema operativo
Resource Group
regione
Public IP, se presente
Virtual network/subnet
Network interface
OS disk
```

Controllare se la VM è:

```text
Running
Stopped
Stopped (deallocated)
```

Evidenza consigliata:

```text
evidence/ud06_portal_vm_overview.png
```

### Vista da CLI

Dettagli VM:

```bash
# Salva i dettagli della VM.
az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_vm_details.json
```

Instance view, inclusivo dello stato runtime:

```bash
# Salva lo stato runtime della VM, incluso il power state.
az vm get-instance-view \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --output json > evidence/ud06_vm_instance_view.json
```

Stato sintetico:

```bash
# Mostra gli stati principali della VM in forma tabellare.
az vm get-instance-view \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query "instanceView.statuses[].{code:code,displayStatus:displayStatus}" \
  --output table
```

Resource ID:

```bash
# Estrae il Resource ID della VM.
export VM_ID="$(az vm show \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query id \
  --output tsv)"
```

## 11.2 Metriche VM

### Vista da Portale Azure

Dal Portale Azure:

```text
Virtual Machine
-> Monitoring
-> Metrics
```

Metriche utili da cercare, se disponibili:

```text
Percentage CPU
Network In
Network Out
Disk Read Bytes
Disk Write Bytes
```

Osservare:

```text
la VM ha dati recenti?
lo stato della VM spiega l'assenza o presenza di dati?
la CPU è coerente con una VM ferma o attiva?
```

Evidenza consigliata:

```text
evidence/ud06_portal_vm_metrics_cpu.png
```

### Vista da CLI

Metriche disponibili:

```bash
# Salva l'elenco delle metriche disponibili per la VM.
az monitor metrics list-definitions \
  --resource "$VM_ID" \
  --output json > evidence/ud06_vm_metric_definitions.json
```

Vista sintetica:

```bash
# Mostra nome, unità e aggregazione primaria delle metriche VM.
az monitor metrics list-definitions \
  --resource "$VM_ID" \
  --query "[].{name:name.value,unit:unit,aggregation:primaryAggregationType}" \
  --output table
```

Valori CPU recenti:

```bash
# Salva valori recenti della metrica Percentage CPU.
az monitor metrics list \
  --resource "$VM_ID" \
  --metric "Percentage CPU" \
  --interval PT5M \
  --output json > evidence/ud06_vm_metric_values.json
```

## 11.3 Diagnostic Settings VM

### Vista da Portale Azure

Dal Portale Azure:

```text
Virtual Machine
-> Monitoring
-> Diagnostic settings
```

Osservare:

```text
sono presenti Diagnostic Settings?
quali categorie sono disponibili?
esiste una destinazione di raccolta?
```

Non creare o modificare Diagnostic Settings in UD06, salvo autorizzazione esplicita del docente.

Evidenza consigliata:

```text
evidence/ud06_portal_vm_diagnostic_settings.png
```

### Vista da CLI

Diagnostic Settings:

```bash
# Salva l'elenco dei Diagnostic Settings esistenti per la VM.
az monitor diagnostic-settings list \
  --resource "$VM_ID" \
  --output json > evidence/ud06_vm_diagnostic_settings.json
```

## 11.4 Interpretazione VM

Nel report rispondere:

```text
La VM è running, stopped o deallocated?
Quali metriche sono disponibili?
La metrica Percentage CPU ha valori recenti?
Lo stato della VM è coerente con le metriche disponibili?
Ci sono risorse collegate da considerare per i costi?
Il Portale e la CLI mostrano informazioni coerenti?
```

---

# Parte G - Tabella di classificazione segnali

## 12. Tabella segnali

Compilare nel report:

| Risorsa | Segnale | Tipo segnale | Dove visto nel Portale | Evidenza CLI | Domanda diagnostica |
|---|---|---|---|---|---|
| Resource Group | Activity Log | amministrativo | `Resource Group -> Activity log` | `ud06_activity_log.json` | quali operazioni recenti ci sono state? |
| Storage | Transactions | metrica | `Storage -> Metrics` | `ud06_storage_metric_values.json` | c'è traffico recente? |
| App Service | Requests | metrica | `App Service -> Metrics` | `ud06_appservice_metric_values.json` | l'app riceve richieste? |
| VM | PowerState | stato operativo | `VM -> Overview` | `ud06_vm_instance_view.json` | la VM consuma compute? |

Adattare la tabella alle risorse effettivamente presenti.

---

# Parte H - Report finale

## 13. Report finale

Compilare:

```text
docs/report_ud06_segnali_diagnostici_azure.md
```

Struttura richiesta:

```markdown
# Report UD06 - Segnali diagnostici risorse Azure

## 1. Contesto

Subscription:
Tenant:
Utente:
Resource Group:
Data/ora:
Risorse analizzate:

## 2. Confronto Portale / CLI

| Task | Vista Portale usata | Comando CLI usato | Evidenza salvata | Coerenza osservata |
|---|---|---|---|---|

## 3. Inventario

Numero risorse:
Tipi risorse:
Risorse collegate:
Risorse inattese:
Screenshot Portale:
Evidenza CLI:

## 4. Activity Log

Operazioni recenti:
Failure rilevate:
Screenshot Portale:
Evidenza CLI:
Interpretazione:

## 5. Storage Account, se presente

Nome:
Stato/proprietà rilevanti:
Metriche disponibili:
Metrica analizzata:
Diagnostic Settings:
Screenshot Portale:
Evidenze CLI:
Interpretazione:

## 6. App Service, se presente

Nome:
Stato:
Hostname:
Metriche disponibili:
Metrica analizzata:
Diagnostic Settings:
Screenshot Portale:
Evidenze CLI:
Interpretazione:

## 7. VM, se presente

Nome:
Power state:
Metriche disponibili:
Metrica analizzata:
Diagnostic Settings:
Screenshot Portale:
Evidenze CLI:
Interpretazione:

## 8. Tabella segnali

| Risorsa | Segnale | Tipo | Domanda diagnostica | Evidenza Portale | Evidenza CLI |
|---|---|---|---|---|---|

## 9. Conclusioni

Cosa posso diagnosticare già oggi:
Cosa non posso ancora diagnosticare:
Cosa servirebbe configurare nelle UD successive:
```

---

# Parte I - Commit e push

## 14. Commit e push

Verificare file prodotti:

```bash
# Mostra i file locali prodotti nel laboratorio.
find docs evidence -maxdepth 2 -type f | sort
```

Verificare git:

```bash
# Mostra file nuovi o modificati.
git status
```

Commit consigliato:

```bash
# Aggiunge report ed evidenze al repository.
git add docs evidence

# Crea un commit con messaggio descrittivo.
git commit -m "Add UD06 Azure diagnostic signals report"

# Invia il commit al repository remoto.
git push
```

---

## 15. Criteri di completamento

Il laboratorio è completato quando:

```text
[ ] il contesto Azure è stato verificato da Portale e CLI
[ ] il Resource Group è stato inventariato da Portale e CLI
[ ] l'Activity Log è stato osservato nel Portale e salvato da CLI
[ ] almeno una risorsa è stata analizzata in dettaglio
[ ] metriche disponibili e valori recenti sono stati verificati
[ ] Diagnostic Settings e categorie sono stati controllati
[ ] il report collega segnali a domande diagnostiche
[ ] sono presenti screenshot o note tratte dal Portale
[ ] sono presenti evidenze JSON prodotte da CLI locale
[ ] commit/push eseguiti, se richiesti
```

---

## 16. Sintesi finale Portale / CLI

| Strumento | Usarlo per | Non usarlo per |
|---|---|---|
| Portale Azure | orientamento, lettura visuale, screenshot, esplorazione | automatizzare evidenze ripetibili |
| Azure CLI locale | esportare JSON, ripetere controlli, produrre evidenze versionabili | capire per la prima volta dove si trova una funzione nel Portale |
| Cloud Shell | verifiche rapide senza redirection, output da copiare | creare file direttamente nel repository locale |

Formula da ricordare:

```text
Portale: capisco dove guardare.
CLI locale: salvo ciò che ho visto.
Report: spiego perché quel segnale conta.
```

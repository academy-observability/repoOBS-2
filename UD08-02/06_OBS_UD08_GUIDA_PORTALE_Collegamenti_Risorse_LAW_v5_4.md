# 06 - Guida portale UD08
## Collegamento delle risorse Azure al Log Analytics Workspace

## Obiettivo

Questa guida spiega come collegare dal **Portale Azure** le risorse create nelle UD precedenti, in particolare UD05, al **Log Analytics Workspace** usato nella UD08.

Lo scopo è far lavorare i partecipanti su **tabelle reali Azure**, non soltanto su dataset simulati con `datatable()`.

Alla fine della procedura sarà possibile interrogare nel LAW tabelle come:

| Sorgente | Tabella KQL attesa |
|---|---|
| Activity Log della subscription | `AzureActivity` |
| Storage Account - Blob service | `StorageBlobLogs` |
| Web App / App Service | `AppServiceHTTPLogs` |
| VM con Azure Monitor Agent | `Heartbeat`, `Perf`, `Syslog`, `Event` |

---

## Concetto fondamentale

Il **Log Analytics Workspace** non raccoglie automaticamente i log delle risorse solo perché si trova nello stesso Resource Group.

Per ogni sorgente bisogna configurare esplicitamente l'invio dei dati verso il LAW.

In pratica:

```text
Risorsa Azure sorgente
    -> diagnostic setting oppure Data Collection Rule
        -> Log Analytics Workspace
            -> tabella KQL reale
```

Il collegamento non si imposta quasi mai entrando nel LAW. Si parte invece dalla **risorsa sorgente** o da **Azure Monitor** e si sceglie il LAW come destinazione.

---

## Esempio docente dalle risorse mostrate in aula

Nell'ambiente docente le risorse osservabili sono, ad esempio:

| Variabile | Valore esempio docente | Significato |
|---|---|---|
| `RG_UD05` | `rg-obs-ud05-ep` | Resource Group con risorse UD05 |
| `LAW` | `law-obs-ud08-ep` | Log Analytics Workspace di destinazione |
| `STORAGE_ACCOUNT` | `stobsud05ep01` | Storage Account da osservare |
| `WEBAPP_NAME` | `app-obs-ud05-ep` | Web App da osservare |
| `VM_NAME` | `vm01` | VM da osservare nella parte opzionale |

Questi valori sono **solo esempi docente**. Ogni partecipante deve usare i propri nomi risorsa.

Configurazione partecipante attesa:

```bash
RG_UD05="<resource-group-ud05-del-partecipante>"
LAW="<law-ud08-del-partecipante>"
STORAGE_ACCOUNT="<storage-account-ud05-del-partecipante>"
CONTAINER_NAME="<container-blob-ud05-del-partecipante>"
WEBAPP_NAME="<web-app-ud05-del-partecipante>"
VM_NAME="<vm-ud05-del-partecipante>"
```

---

# 1 - Activity Log subscription verso LAW

## Risorsa sorgente

La sorgente è l'**Activity Log della subscription**.

Non è una risorsa del Resource Group. Per questo motivo il collegamento non si configura entrando nel Resource Group, ma dalla subscription o da Azure Monitor.

## Tabella KQL attesa

```kusto
AzureActivity
```

## Percorso da Portale Azure

Usare uno dei due percorsi.

Percorso consigliato da Azure Monitor:

```text
Azure Portal
-> Monitor
-> Activity log
-> Export Activity Logs
-> Add diagnostic setting
```

Percorso alternativo dalla subscription:

```text
Azure Portal
-> Subscriptions
-> selezionare la subscription del corso
-> Activity log
-> Export Activity Logs
-> Add diagnostic setting
```

## Configurazione

| Campo | Valore consigliato |
|---|---|
| Diagnostic setting name | `ds-ud08-activity-to-law` |
| Category minima | `Administrative` |
| Altre categorie utili | `Security`, `ServiceHealth`, `Policy`, `Recommendation`, `ResourceHealth`, `Alert` |
| Destination details | `Send to Log Analytics workspace` |
| Log Analytics Workspace | LAW UD08 del partecipante |

Confermare con:

```text
Save
```

## Generazione evento amministrativo

Dopo aver creato il diagnostic setting, bisogna generare un evento amministrativo.

Esempi:

- aggiornare un tag del Resource Group;
- avviare o arrestare una VM;
- modificare una configurazione non critica;
- creare o eliminare una risorsa temporanea.

## Query di verifica

```kusto
AzureActivity
| where TimeGenerated > ago(2h)
| project TimeGenerated, ResourceGroup, ResourceProvider, OperationNameValue, ActivityStatusValue, Caller
| sort by TimeGenerated desc
| take 20
```

Query di conteggio:

```kusto
AzureActivity
| where TimeGenerated > ago(2h)
| count
```

---

# 2 - Storage Account Blob service verso LAW

## Risorsa sorgente

La sorgente non è genericamente lo Storage Account, ma il servizio:

```text
Storage Account
-> Blob service
```

Nel caso docente:

```text
Storage Account: stobsud05ep01
Servizio: Blob
LAW: law-obs-ud08-ep
```

## Tabella KQL attesa

```kusto
StorageBlobLogs
```

## Percorso da Portale Azure

```text
Azure Portal
-> Resource groups
-> selezionare il Resource Group UD05
-> selezionare lo Storage Account
-> Monitoring
-> Diagnostic settings
```

Se il portale mostra la scelta del servizio Storage, selezionare:

```text
Blob
```

Poi:

```text
Add diagnostic setting
```

## Configurazione

| Campo | Valore consigliato |
|---|---|
| Diagnostic setting name | `ds-ud08-blob-to-law` |
| Log categories | `StorageRead`, `StorageWrite`, `StorageDelete` |
| Destination details | `Send to Log Analytics workspace` |
| Log Analytics Workspace | LAW UD08 del partecipante |
| Destination table | `Resource specific`, se disponibile |

Confermare con:

```text
Save
```

## Generazione traffico Blob

Dopo il collegamento, bisogna generare traffico sul container Blob.

Operazioni utili:

- upload di un file;
- list dei blob;
- download di un file;
- delete di un file.

Senza traffico successivo alla configurazione del diagnostic setting, la tabella può rimanere vuota.

## Query di verifica

```kusto
StorageBlobLogs
| where TimeGenerated > ago(2h)
| project TimeGenerated, AccountName, OperationName, StatusCode, Uri, CallerIpAddress
| sort by TimeGenerated desc
| take 20
```

Query di conteggio:

```kusto
StorageBlobLogs
| where TimeGenerated > ago(2h)
| count
```

---

# 3 - Web App / App Service verso LAW

## Risorsa sorgente

La sorgente è la **Web App**, non l'App Service Plan.

Nel caso docente:

```text
Web App: app-obs-ud05-ep
LAW: law-obs-ud08-ep
```

L'App Service Plan è importante per l'esecuzione dell'applicazione, ma non è la sorgente principale da collegare in questo laboratorio.

## Tabella KQL attesa

```kusto
AppServiceHTTPLogs
```

Altre tabelle possibili, se le categorie sono abilitate e supportate:

```kusto
AppServiceConsoleLogs
AppServiceAppLogs
AppServiceAuditLogs
AppServicePlatformLogs
```

## Percorso da Portale Azure

```text
Azure Portal
-> Resource groups
-> selezionare il Resource Group UD05
-> selezionare la Web App
-> Monitoring
-> Diagnostic settings
-> Add diagnostic setting
```

## Configurazione

| Campo | Valore consigliato |
|---|---|
| Diagnostic setting name | `ds-ud08-webapp-to-law` |
| Categoria minima | `AppServiceHTTPLogs` |
| Altre categorie utili | `AppServiceConsoleLogs`, `AppServiceAppLogs`, `AppServiceAuditLogs`, `AppServicePlatformLogs` |
| Destination details | `Send to Log Analytics workspace` |
| Log Analytics Workspace | LAW UD08 del partecipante |
| Destination table | `Resource specific`, se disponibile |

Confermare con:

```text
Save
```

## Generazione traffico HTTP

Dopo il collegamento, bisogna generare richieste verso la Web App.

Esempi:

- aprire la Web App dal browser;
- richiamare più volte l'URL pubblico;
- richiamare un percorso inesistente per generare un possibile `404`.

Esempio di URL:

```text
https://<nome-webapp>.azurewebsites.net/
```

Non costruire l'URL a memoria durante il laboratorio: è preferibile copiarlo dal valore `Default domain` o `Default hostname` della Web App.

## Query di verifica

```kusto
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| project TimeGenerated, CsHost, CsMethod, CsUriStem, ScStatus, TimeTaken, CIp
| sort by TimeGenerated desc
| take 20
```

Query di conteggio:

```kusto
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| count
```

---

# 4 - VM verso LAW con Azure Monitor Agent e DCR

## Risorsa sorgente

La sorgente è la **VM**, ma per le VM il collegamento non avviene normalmente con un semplice diagnostic setting.

Il modello corretto è:

```text
Azure Monitor Agent
+ Data Collection Rule
+ associazione della DCR alla VM
+ destinazione Log Analytics Workspace
```

Questa parte è consigliata come estensione opzionale perché richiede più tempo operativo.

## Tabelle KQL attese

| Sistema operativo | Tabelle attese |
|---|---|
| Linux | `Heartbeat`, `Perf`, `Syslog` |
| Windows | `Heartbeat`, `Perf`, `Event` |

## Percorso da Portale Azure

```text
Azure Portal
-> Monitor
-> Data Collection Rules
-> Create
```

## Configurazione base

### Basics

| Campo | Valore consigliato |
|---|---|
| Rule name | `dcr-ud08-vm-basic` |
| Subscription | subscription del corso |
| Resource group | Resource Group UD05 del partecipante |
| Region | regione compatibile con VM e LAW |

### Resources

```text
Add resources
-> selezionare la VM UD05
```

### Collect and deliver

Per VM Linux selezionare:

```text
Syslog
Performance counters
```

Per VM Windows selezionare:

```text
Windows Event Logs
Performance counters
```

Come destinazione scegliere:

```text
Destination type: Azure Monitor Logs / Log Analytics workspace
Workspace: LAW UD08 del partecipante
```

Confermare con:

```text
Review + create
-> Create
```

Durante la creazione o associazione della DCR, Azure può installare automaticamente Azure Monitor Agent sulla VM, se necessario.

## Query di verifica Heartbeat

```kusto
Heartbeat
| where TimeGenerated > ago(2h)
| project TimeGenerated, Computer, OSType, ResourceGroup, _ResourceId
| sort by TimeGenerated desc
| take 20
```

## Query di verifica Performance counters

```kusto
Perf
| where TimeGenerated > ago(2h)
| summarize AvgValue = avg(CounterValue) by Computer, ObjectName, CounterName, bin(TimeGenerated, 5m)
| sort by TimeGenerated desc
| take 50
```

## Query Linux Syslog

```kusto
Syslog
| where TimeGenerated > ago(2h)
| project TimeGenerated, Computer, Facility, SeverityLevel, SyslogMessage
| sort by TimeGenerated desc
| take 30
```

## Query Windows Event Log

```kusto
Event
| where TimeGenerated > ago(2h)
| project TimeGenerated, Computer, EventLog, EventID, Source, RenderedDescription
| sort by TimeGenerated desc
| take 30
```

---

# 5 - Risorse da non collegare in questo laboratorio

Nel Resource Group possono comparire molte risorse correlate alla VM o alla Web App. Non tutte sono sorgenti principali per questo laboratorio.

| Risorsa | Motivo |
|---|---|
| App Service Plan | non è la sorgente HTTP principale; osserviamo la Web App |
| Public IP | non è necessario nel percorso base UD08 |
| Network Interface | non è necessario nel percorso base UD08 |
| Virtual Network | non è necessario nel percorso base UD08 |
| Network Security Group | utile per estensioni su NSG flow logs, ma non nel percorso base |
| Disk della VM | non è sorgente principale nel laboratorio |
| NetworkWatcherRG | non è il workload applicativo del partecipante |

Per il laboratorio UD08 base le sorgenti principali sono:

```text
subscription Activity Log
Storage Account Blob service
Web App / App Service
VM opzionale con AMA + DCR
```

---

# 6 - Riepilogo collegamenti risorsa-LAW

| Risorsa | Dove configurare da portale | Meccanismo | Destinazione | Tabella attesa |
|---|---|---|---|---|
| Activity Log subscription | `Monitor -> Activity log -> Export Activity Logs` | Diagnostic setting subscription | LAW UD08 | `AzureActivity` |
| Storage Blob | `Storage Account -> Monitoring -> Diagnostic settings -> Blob` | Diagnostic setting sul Blob service | LAW UD08 | `StorageBlobLogs` |
| Web App | `Web App -> Monitoring -> Diagnostic settings` | Diagnostic setting sulla Web App | LAW UD08 | `AppServiceHTTPLogs` |
| VM | `Monitor -> Data Collection Rules -> Create` | AMA + DCR + associazione alla VM | LAW UD08 | `Heartbeat`, `Perf`, `Syslog`, `Event` |

---

# 7 - Verifiche finali nel LAW

Dopo avere configurato i collegamenti e generato traffico, aprire:

```text
Azure Portal
-> Log Analytics Workspaces
-> selezionare il LAW UD08
-> Logs
```

Eseguire le query di controllo.

## Activity Log

```kusto
AzureActivity
| where TimeGenerated > ago(24h)
| count
```

## Storage Blob

```kusto
StorageBlobLogs
| where TimeGenerated > ago(24h)
| count
```

## Web App

```kusto
AppServiceHTTPLogs
| where TimeGenerated > ago(24h)
| count
```

## VM

```kusto
Heartbeat
| where TimeGenerated > ago(24h)
| count
```

---

# 8 - Interpretazione dei risultati

## Query valida ma risultato vuoto

Esempio:

```json
[]
```

Significa che la tabella è interrogabile, ma nel periodo selezionato non ci sono righe restituite.

Azioni:

- aumentare il time range a 24 ore;
- verificare di avere generato traffico dopo il diagnostic setting;
- attendere qualche minuto per l'ingestione;
- controllare di interrogare il LAW corretto.

## Errore: tabella non risolta

Esempio:

```text
Failed to resolve table or column expression
```

Possibili cause:

- la sorgente non è mai stata collegata al LAW;
- il diagnostic setting è stato creato sulla risorsa sbagliata;
- la categoria log non è stata abilitata;
- non è ancora arrivato nessun dato;
- si sta usando una tabella diversa da quella prodotta dalla modalità configurata.

## Nessun dato dopo il collegamento

Controllare:

- diagnostic setting presente sulla risorsa sorgente;
- LAW di destinazione corretto;
- categorie log abilitate;
- traffico generato dopo la configurazione;
- finestra temporale della query;
- eventuale ritardo di ingestione.

---

# 9 - Messaggio didattico da enfatizzare

Il LAW è il punto di raccolta e interrogazione, ma non osserva automaticamente tutto.

Per ottenere tabelle reali Azure servono tre passaggi:

```text
1. collegare la sorgente al LAW
2. generare eventi o traffico
3. interrogare la tabella KQL corretta
```

Esempio:

```text
Web App
-> diagnostic setting verso LAW
-> richieste HTTP
-> AppServiceHTTPLogs
```

Esempio:

```text
Storage Blob
-> diagnostic setting verso LAW
-> upload/list/download/delete
-> StorageBlobLogs
```

Esempio:

```text
VM
-> Azure Monitor Agent + DCR
-> raccolta guest OS
-> Heartbeat / Perf / Syslog / Event
```

---

# 10 - Evidenze consigliate

Ogni partecipante dovrebbe salvare screenshot o file di evidenza per:

| Evidenza | Descrizione |
|---|---|
| Diagnostic setting Activity Log | schermata export Activity Logs verso LAW |
| Diagnostic setting Blob | schermata Storage Blob diagnostic setting |
| Diagnostic setting Web App | schermata Web App diagnostic setting |
| Query `AzureActivity` | risultato o count |
| Query `StorageBlobLogs` | risultato o count |
| Query `AppServiceHTTPLogs` | risultato o count |
| DCR VM, se svolta | schermata Data Collection Rule e associazione VM |
| Query `Heartbeat`, se svolta | risultato o count |

---

## Criteri di completamento

| Criterio | Stato |
|---|---|
| Activity Log collegato al LAW | ☐ |
| Evento amministrativo generato | ☐ |
| Query `AzureActivity` eseguita | ☐ |
| Blob service collegato al LAW | ☐ |
| Traffico Blob generato | ☐ |
| Query `StorageBlobLogs` eseguita | ☐ |
| Web App collegata al LAW | ☐ |
| Traffico HTTP generato | ☐ |
| Query `AppServiceHTTPLogs` eseguita | ☐ |
| VM collegata con AMA + DCR, se prevista | ☐ |
| Query `Heartbeat` / `Perf` / `Syslog` / `Event` eseguite, se previste | ☐ |
| Risultati vuoti interpretati correttamente | ☐ |
| Evidenze salvate | ☐ |

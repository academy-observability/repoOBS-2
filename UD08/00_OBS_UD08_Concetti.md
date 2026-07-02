# UD08 - Concetti 
## Log Analytics Workspace e KQL base

## 1. Perché introduciamo Log Analytics

Nelle UD precedenti abbiamo osservato risorse Azure, Activity Log, metriche, raccolta dati verso Log Analytics e impostazioni di monitoraggio. In UD08 iniziamo a lavorare con una componente centrale dell'osservabilità in Azure: il **Log Analytics Workspace**.

Un Log Analytics Workspace è un ambiente in cui vengono conservati e interrogati dati raccolti da Azure Monitor e da altre sorgenti compatibili. Nel laboratorio lo usiamo soprattutto come **motore di query** per imparare KQL e per preparare le UD successive.

La domanda guida della UD08 è:

```text
Come passo da un segnale osservato nel Portale a una query tecnica, ripetibile e documentabile?
```

## 2. Workspace, tabella, record, colonna

Per leggere correttamente un risultato KQL bisogna distinguere quattro livelli.

| Concetto | Significato | Esempio |
|---|---|---|
| Workspace | contenitore logico dei dati interrogabili | `law-obs-ud08-ep` |
| Tabella | insieme di record con schema comune | `Usage`, `AzureActivity`, `AppServiceHTTPLogs`, `Heartbeat` |
| Record | singola riga della tabella | un evento o una misura registrata |
| Colonna | attributo del record | `TimeGenerated`, `ResourceGroup`, `DataType` |

Una query KQL non interroga genericamente "Azure". Interroga dati disponibili nello **scope** selezionato, normalmente un workspace o una risorsa.

## 3. Nome workspace, Resource ID e customerId

Nel laboratorio incontriamo tre identificativi diversi.

| Identificativo | A cosa serve |
|---|---|
| Nome workspace | nome della risorsa Azure visibile nel Portale |
| Resource ID | percorso ARM completo della risorsa |
| `customerId` / Workspace ID | identificativo usato da CLI/API per eseguire query Log Analytics |

Nel Portale si lavora quasi sempre con il nome della risorsa. Da Azure CLI, per `az monitor log-analytics query`, useremo il `customerId`.

## 4. Scope e time range

Ogni query deve avere uno scope e un intervallo temporale coerente.

| Elemento | Domanda a cui risponde |
|---|---|
| Scope | su quale workspace o risorsa sto interrogando? |
| Time range | quale finestra temporale sto analizzando? |
| Query | quali righe e colonne voglio leggere o aggregare? |

Un errore comune è scrivere una query corretta ma guardare un time range in cui non esistono dati. In quel caso il risultato vuoto non indica automaticamente un problema: può indicare semplicemente che non ci sono record nella finestra scelta.

## 5. KQL: struttura mentale di base

KQL lavora spesso come una pipeline:

```kql
// La tabella iniziale fornisce le righe di partenza.
NomeTabella
// where filtra le righe.
| where TimeGenerated > ago(1d)
// project seleziona le colonne da mostrare.
| project TimeGenerated, ResourceGroup, OperationName
// sort ordina il risultato.
| sort by TimeGenerated desc
```

Ogni riga dopo il simbolo `|` riceve il risultato dello step precedente e lo trasforma.

## 6. Operatori usati in UD08

| Operatore | Uso nel laboratorio |
|---|---|
| `datatable` | crea dati simulati per esercitarsi anche con workspace vuoto |
| `take` | limita il numero di righe mostrate |
| `where` | filtra righe in base a condizioni |
| `project` | seleziona e riordina colonne |
| `sort by` | ordina i risultati |
| `summarize` | aggrega più righe in valori riassuntivi |
| `count()` | conta righe |
| `countif()` | conta righe che rispettano una condizione |
| `avg()` | calcola una media |
| `max()` | calcola il massimo |
| `ago()` | definisce finestre temporali relative |

## 7. Query simulata e query reale

In UD08 usiamo due tipi di query.

| Tipo | Esempio | Valore didattico |
|---|---|---|
| Query simulata | `datatable(...)` | permette di imparare KQL anche se il workspace ha pochi dati |
| Query reale | `Usage`, `AzureActivity`, `AppServiceHTTPLogs`, `Heartbeat` | legge dati presenti nel workspace |

La query simulata è utile per imparare l'operatore. La query reale è utile per osservare un ambiente effettivo.

Le due cose non vanno confuse: una query con `datatable` non dimostra che una risorsa reale ha generato log.

## 8. La tabella `Usage`

La tabella `Usage`, quando disponibile, aiuta a capire quali tipi di dati sono presenti nel workspace e in quale quantità.

Esempio concettuale:

```kql
// La tabella Usage descrive la presenza di dati nel workspace.
Usage
// Limita l'analisi agli ultimi sette giorni.
| where TimeGenerated > ago(7d)
// Raggruppa per tipo di dato e somma la quantità.
| summarize QuantitaTotale=sum(Quantity) by DataType
// Mostra prima i tipi di dato più presenti.
| sort by QuantitaTotale desc
```

Se la tabella non restituisce righe, le cause più frequenti sono workspace appena creato, nessuna raccolta dati attiva o time range non adatto.


## Nota aggiornata su Diagnostic settings, VM, Insights e DCR

Nel percorso Azure usiamo il termine **raccolta dati** in senso ampio. Non tutti i servizi espongono lo stesso percorso nel portale e non tutte le tabelle compaiono nello stesso modo nel Log Analytics Workspace.

Per le **macchine virtuali** non trattiamo come percorso standard la vecchia esperienza legata alla Azure Diagnostics Extension. Per i dati guest della VM, come heartbeat, performance counter, eventi Windows o syslog Linux, il riferimento operativo del corso è **Azure Monitor Agent**, eventualmente abilitato tramite **VM Insights / Enhanced monitoring**, e configurato tramite **Data Collection Rules**.

Per altri servizi Azure, come App Service, Storage o risorse PaaS, i **Diagnostic settings** restano invece un meccanismo comune per inviare resource logs verso Log Analytics quando il servizio li supporta.

Quindi nei laboratori UD08-UD10 non assumiamo una tabella unica sempre presente. Prima scopriamo le tabelle effettivamente popolate, poi scegliamo il ramo corretto:

| Caso | Tabelle tipiche | Lettura didattica |
|---|---|---|
| Attività amministrativa | `AzureActivity` | Operazioni sul piano di controllo Azure |
| Metriche esportate | `AzureMetrics` | Campioni metrici inviati al workspace, se configurati |
| App Service | `AppServiceHTTPLogs`, `AppServiceAppLogs`, `AppServiceConsoleLogs` | Traffico HTTP e log applicativi PaaS |
| VM con AMA/DCR | `Heartbeat`, `Perf`, `InsightsMetrics`, `Event`, `Syslog` | Segnali guest raccolti dall'agente moderno |
| Risorse o configurazioni legacy/generiche | `AzureDiagnostics` | Resource logs in schema generico |
| Workspace povero di dati | `Usage` e query `datatable()` | Palestra KQL e verifica ingestione |

## 9. La tabella `AzureActivity`

`AzureActivity` può contenere eventi amministrativi Azure inviati al workspace. Non è garantito che sia presente o popolata in ogni ambiente.

Esempio concettuale:

```kql
// AzureActivity contiene eventi amministrativi quando sono raccolti nel workspace.
AzureActivity
// Limita la lettura agli ultimi sette giorni.
| where TimeGenerated > ago(7d)
// Mostra colonne utili per una prima analisi.
| project TimeGenerated, ResourceGroup, OperationNameValue, ActivityStatusValue, Caller
// Porta in alto gli eventi più recenti.
| sort by TimeGenerated desc
| take 20
```

Se `AzureActivity` non è disponibile, il laboratorio resta valido usando `datatable` e tabelle realmente presenti nel workspace.

## 10. Risultato vuoto, tabella assente, errore di query

| Situazione | Significato probabile | Azione tecnica |
|---|---|---|
| Query corretta, zero righe | non ci sono dati nel time range | aumentare o modificare il time range e documentare l'esito |
| Tabella non trovata | la sorgente non è stata raccolta nel workspace | usare `Usage` o `datatable`, documentando la tabella assente |
| Errore di sintassi | KQL non valido | leggere messaggio, correggere operatore o nome colonna |
| Access denied | ruolo o subscription non coerenti | verificare account, subscription e permessi sulla risorsa |

## 11. Portale e CLI hanno ruoli diversi

| Strumento | Ruolo |
|---|---|
| Portale Azure | orientarsi, vedere schema, tabelle, query editor e risultati |
| CLI locale | salvare evidenze JSON ripetibili nel repository |
| File `.kql` | rendere una query riutilizzabile e revisionabile |
| Report | spiegare il significato tecnico del risultato |

Cloud Shell può essere utile per prove rapide, ma non sostituisce il repository locale quando bisogna produrre file in `docs/`, `evidence/`, `logs/` o `img/`.

## 12. Procedura quando manca un prerequisito

| Prerequisito mancante | Procedura |
|---|---|
| Azure CLI assente | installare Azure CLI in WSL o usare un terminale locale già configurato |
| login Azure assente | eseguire `az login --use-device-code` |
| subscription errata | usare `az account list -o table` e poi `az account set --subscription "<id>"` |
| file `config/ud08.env` assente | copiare `config/ud08.env.example` in `config/ud08.env` e valorizzare i campi |
| workspace assente | creare un workspace dedicato UD08 con la procedura del laboratorio |
| comando query CLI non disponibile | usare il Portale per esecuzione e screenshot, poi aggiornare Azure CLI prima di riprovare la parte JSON |

## 13. Cosa deve risultare chiaro prima del laboratorio

Alla fine della parte concettuale dobbiamo saper rispondere a queste domande:

1. Che cos'è un Log Analytics Workspace?
2. Perché il nome del workspace non coincide con il `WORKSPACE_ID`?
3. Che differenza c'è tra query simulata e query reale?
4. Perché un risultato vuoto non indica automaticamente un errore?
5. Perché `where`, `project` e `summarize` rispondono a domande diverse?
6. Perché salviamo query e risultati nel repository?

# OBS_UD07 - Concetti dettagliati v4

# Azure Monitor, metriche, Diagnostic Settings e generazione controllata di segnali

## 1. Collocazione della UD07

La sequenza didattica è questa:

```text
UD05 = creiamo e classifichiamo risorse Azure IaaS/PaaS/SaaS.
UD06 = osserviamo quali segnali diagnostici espongono le risorse.
UD07 = generiamo segnali controllati, leggiamo metriche e interpretiamo prima/dopo.
UD08 = iniziamo a interrogare dati centralizzati in Log Analytics con KQL.
```

UD07 non deve ripetere UD06. Il punto non è rifare l'inventario completo del Resource Group, ma usare alcune risorse già note per capire meglio **metriche, aggregazioni, Activity Log e Diagnostic Settings**.

La domanda guida cambia:

```text
UD06: quali segnali esistono?
UD07: cosa succede al segnale se genero attività controllata?
```

Questa piccola differenza evita di trasformare Azure Monitor in una visita guidata tra menu, cosa che l'umanità non merita due volte nella stessa settimana.

## 2. Azure Monitor in questa unità

Azure Monitor è il servizio Azure usato per raccogliere, visualizzare, analizzare e instradare dati di monitoraggio.

In UD07 lo usiamo soprattutto per:

```text
leggere metriche di piattaforma;
confrontare time range e granularità;
confrontare aggregazioni;
osservare Activity Log;
verificare categorie diagnostiche;
verificare Diagnostic Settings esistenti;
preparare il passaggio a Log Analytics e KQL.
```

Azure Monitor non è una sola schermata. È una famiglia di funzionalità: Metrics, Activity Log, Logs, Diagnostic Settings, Alerts, Workbooks e integrazioni con Application Insights o altri strumenti.

## 3. Metriche

Una metrica è un valore numerico osservato nel tempo.

Esempi:

| Risorsa | Metrica | Domanda diagnostica |
|---|---|---|
| App Service | `Requests` | l'app riceve traffico? |
| Storage Account | `Transactions` | lo storage viene usato? |
| VM | `Percentage CPU` | la VM ha carico CPU? |
| Public IP | `Byte Count` o metrica equivalente | passa traffico? |

Una metrica non è utile da sola. Diventa utile quando risponde a una domanda.

Esempio sbagliato:

```text
Ho visto la metrica Requests.
```

Esempio corretto:

```text
Ho osservato Requests sull'App Service dopo aver generato richieste HTTP.
La metrica mostra traffico nel time range osservato, quindi l'applicazione è stata raggiunta.
```

## 4. Serie temporale

Le metriche sono serie temporali. Ogni punto ha almeno:

```text
timestamp;
nome della metrica;
valore;
aggregazione;
risorsa associata;
eventuali dimensioni.
```

La serie temporale permette di vedere se un fenomeno cambia nel tempo. In UD07 osserviamo soprattutto la differenza tra:

```text
prima della generazione traffico;
dopo la generazione traffico.
```

## 5. Time range e interval

Nel Portale Azure scegliamo un **time range**, per esempio `Last hour`.

Da CLI usiamo spesso `--interval`, per esempio:

```bash
az monitor metrics list \
  --resource "$APP_ID" \
  --metric "Requests" \
  --interval PT1M \
  --aggregation Total
```

`--interval PT1M` indica la granularità dei punti restituiti, non significa automaticamente “ultimi 1 minuto”. Il time range complessivo può essere implicito o specificato con parametri aggiuntivi, a seconda del comando usato.

Questa distinzione è piccola, ma ha già rovinato più report di quanto sia socialmente accettabile.

## 6. Aggregazioni

Una metrica può essere letta con aggregazioni diverse.

| Aggregazione | Significato pratico | Quando è utile |
|---|---|---|
| `Average` | valore medio nell'intervallo | carico medio, andamento generale |
| `Maximum` | valore massimo nell'intervallo | picchi, saturazioni brevi |
| `Minimum` | valore minimo nell'intervallo | cali, disponibilità, soglie basse |
| `Total` | somma dei valori nell'intervallo | conteggi, richieste, transazioni |
| `Count` | numero di campioni | presenza di dati, quantità di misurazioni |

Esempio:

```text
Per Requests su App Service uso spesso Total.
Per Percentage CPU su VM confronto Average e Maximum.
```

Average può nascondere picchi brevi. Maximum può evidenziarli. Total è più adatto per conteggi come richieste o transazioni.

## 7. Metric definitions e metric values

In UD07 distinguiamo due cose:

| Elemento | Domanda a cui risponde |
|---|---|
| Metric definitions | quali metriche espone questa risorsa? |
| Metric values | quali valori ha prodotto una metrica in un certo periodo? |

Una risorsa può esporre una metrica anche se non ha valori recenti. Per esempio, un App Service può esporre `Requests`, ma se nessuno lo visita nel time range scelto il grafico può risultare vuoto.

Quindi:

```text
definizione metrica disponibile ≠ traffico reale presente
```

## 8. Activity Log

Activity Log registra operazioni amministrative sul piano di controllo Azure.

Esempi:

```text
creazione risorsa;
modifica tag;
start/stop di una VM;
modifica configurazione;
operazioni riuscite o fallite del Resource Manager.
```

Activity Log non è il log applicativo. Se aggiorniamo un tag su un App Service, vediamo un evento amministrativo. Non stiamo dimostrando che l'app riceve traffico.

Distinzione essenziale:

| Segnale | Piano | Esempio |
|---|---|---|
| Activity Log | control plane | modifico tag, creo VM, cambio configurazione |
| Resource logs | data plane / comportamento risorsa | richieste, errori, operazioni interne della risorsa |
| Metriche | valori numerici nel tempo | Requests, Transactions, CPU |

## 9. Diagnostic Settings

Diagnostic Settings serve a instradare log e metriche supportate da una risorsa verso destinazioni come:

```text
Log Analytics Workspace;
Storage Account;
Event Hub;
partner solution, se disponibile.
```

In UD07 non è obbligatorio creare Diagnostic Settings. L'obiettivo minimo è capire:

```text
quali categorie diagnostiche sono disponibili;
se esistono già Diagnostic Settings;
quale destinazione avrebbe senso usare nelle UD successive.
```

La configurazione effettiva può essere rimandata a UD08, quando Log Analytics diventa centrale.

## 10. Segnali generati intenzionalmente

La novità v4 è l'introduzione di attività controllate per generare segnali osservabili.

Usiamo due tipi di script:

| Script | Cosa genera | Dove si osserva |
|---|---|---|
| amministrativo | aggiornamento tag su risorse core | Activity Log, Tags |
| applicativo/workload | richieste HTTP, operazioni blob, CPU VM opzionale | Metrics Explorer e Azure Monitor Metrics |

Questa distinzione è il cuore della UD07.

```text
Aggiornare tag genera Activity Log.
Chiamare l'App Service genera Requests.
Fare upload/list/download/delete blob genera Transactions.
Generare carico CPU nella VM può generare Percentage CPU.
```

## 11. Baseline e confronto prima/dopo

Prima di generare traffico, osserviamo la baseline.

Dopo aver generato traffico, osserviamo di nuovo.

Schema:

```text
1. scelgo una risorsa;
2. scelgo una metrica;
3. osservo baseline;
4. genero attività controllata;
5. osservo dopo;
6. confronto;
7. interpreto;
8. salvo evidenze.
```

Questa è osservabilità applicata, non semplice turismo nel Portale Azure.

## 12. Esempi di interpretazione

### App Service

Domanda:

```text
L'app riceve traffico?
```

Segnale:

```text
Requests
```

Interpretazione:

```text
Dopo lo script applicativo mi aspetto un aumento di Requests.
Se non vedo dati subito, posso attendere qualche minuto, verificare il time range e controllare che l'hostname risponda.
```

### Storage Account

Domanda:

```text
Lo Storage Account è stato usato?
```

Segnale:

```text
Transactions
```

Interpretazione:

```text
Dopo operazioni blob di upload, list, download e delete mi aspetto transazioni nel periodo osservato.
```

### VM

Domanda:

```text
La VM ha avuto carico CPU?
```

Segnale:

```text
Percentage CPU
```

Interpretazione:

```text
Se la VM è running e RunCommand riesce, posso osservare Average e Maximum.
Maximum è utile per intercettare picchi brevi.
```

### Activity Log

Domanda:

```text
Quali operazioni amministrative sono state eseguite?
```

Segnale:

```text
Activity Log
```

Interpretazione:

```text
Dopo lo script amministrativo vedo eventi di modifica tag sulle risorse core.
Questo non prova traffico applicativo, ma prova attività sul piano di controllo.
```

## 13. Limiti e possibili anomalie

Durante UD07 possono comparire situazioni non perfette:

| Situazione | Interpretazione |
|---|---|
| Metriche non visibili subito | possibile latenza di Azure Monitor |
| Requests vuota | nessun traffico, time range errato, app non raggiunta o metrica non aggiornata |
| Diagnostic Settings non si carica | provider, permessi, token o problema del Portale |
| VM RunCommand fallisce | VM spenta, permessi, agente, API version o stato non idoneo |
| Storage key non recuperabile | permessi insufficienti sullo Storage Account |
| Activity Log in ritardo | propagazione non immediata |

Il laboratorio non fallisce quando Azure produce un'anomalia. L'anomalia va documentata. D'altra parte, il cloud è nato per trasformare problemi semplici in distribuzioni geografiche.

## 14. Cosa deve saper fare il partecipante alla fine

Alla fine di UD07, il partecipante deve saper:

```text
scegliere una metrica coerente con una domanda tecnica;
usare Metrics Explorer dal Portale;
estrarre definizioni e valori metrici da CLI;
distinguere Activity Log da traffico applicativo;
generare un segnale controllato;
confrontare prima/dopo;
interpretare assenza o presenza di dati;
verificare categorie e Diagnostic Settings;
documentare evidenze e limiti nel report.
```

## 15. Riferimenti ufficiali

- Azure Monitor Metrics overview: https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/data-platform-metrics
- Activity Log in Azure Monitor: https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log
- Diagnostic Settings in Azure Monitor: https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings

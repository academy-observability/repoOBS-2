# UD08 - Laboratorio guidato aggiuntivo: KQL su tabelle Azure reali

Questo laboratorio affianca le query basate su `datatable()`. I dataset locali restano utili per imparare la sintassi KQL in modo deterministico; qui invece lavoriamo sui dati realmente disponibili nel Log Analytics Workspace creato e usato nelle UD precedenti.

L'obiettivo non è ottenere lo stesso risultato per tutti, ma applicare lo stesso metodo:

1. scoprire quali tabelle hanno dati;
2. scegliere la tabella coerente con la domanda;
3. eseguire query semplici e commentate;
4. documentare anche il caso in cui una tabella sia assente o vuota.

## 1. Dove eseguire le query

Eseguire le query da **Azure Portal**:

```text
Log Analytics Workspace → Logs
```

I file `.kql` si trovano nella repository locale, nella cartella:

```text
src/kql/azure/
```

La query può essere copiata dal file `.kql` e incollata nel Logs editor del portale. Le evidenze si salvano poi nella cartella `evidence/` della repository locale. La cartella `evidence/` è nel terminale locale o WSL, non in Azure Cloud Shell.

## 2. Scoperta delle tabelle disponibili

Aprire ed eseguire:

```text
src/kql/azure/01_scopri_tabelle_note_workspace.kql
```

La query cerca tabelle comuni del percorso:

| Area | Tabelle |
|---|---|
| Workspace e ingestione | `Usage` |
| Attività amministrativa Azure | `AzureActivity` |
| Metriche esportate | `AzureMetrics` |
| App Service | `AppServiceHTTPLogs`, `AppServiceAppLogs`, `AppServiceConsoleLogs` |
| VM con Azure Monitor Agent / DCR | `Heartbeat`, `Perf`, `InsightsMetrics`, `Event`, `Syslog` |
| Resource logs generici o legacy | `AzureDiagnostics` |

Annotare nel report quali tabelle risultano presenti, quante righe hanno prodotto e qual è l'ultimo evento osservato.

## 3. Query reale su Usage

Se `Usage` è presente, eseguire:

```text
src/kql/azure/02_usage_summary.kql
```

Questa query non descrive una singola risorsa applicativa. Serve a capire quali tipi di dati sono stati ingeriti nel workspace negli ultimi giorni. È quindi una query di orientamento prima di passare alle tabelle operative.

## 4. Query reale su AzureActivity

Se `AzureActivity` è presente, eseguire:

```text
src/kql/azure/03_azureactivity_attivita_recenti.kql
src/kql/azure/04_azureactivity_operazioni_per_stato.kql
```

La prima query risponde alla domanda: **quali operazioni amministrative sono state registrate di recente?**

La seconda query risponde alla domanda: **come sono distribuite le operazioni per stato?**

Questa è la traduzione reale di un esercizio visto con `datatable()`: non cambia l'operatore KQL, cambia il significato operativo del dato.

## 5. Query reale su metriche esportate

Se `AzureMetrics` è presente, eseguire:

```text
src/kql/azure/05_azuremetrics_metriche_disponibili.kql
```

La tabella può essere vuota. In quel caso non è un errore KQL: significa che nel workspace non sono disponibili metriche esportate per il periodo scelto.

## 6. Query reale su App Service

Se è presente `AppServiceHTTPLogs`, eseguire:

```text
src/kql/azure/06_appservice_http_status.kql
```

Questa query permette di vedere se le chiamate HTTP generate sulle App Service delle UD precedenti hanno prodotto log interrogabili.

## 7. Query reale su VM monitorate con AMA/DCR

Per le VM non usiamo come percorso standard la vecchia diagnostica VM legacy. Se la VM è stata collegata ad Azure Monitor Agent, VM Insights, Enhanced monitoring o a una Data Collection Rule, eseguire:

```text
src/kql/azure/07_vm_ama_dcr_tabelle_disponibili.kql
```

Se non compaiono `Heartbeat`, `Perf`, `InsightsMetrics`, `Event` o `Syslog`, documentare semplicemente che la raccolta guest della VM non è attiva nel workspace.

## 8. Evidenze da produrre

Compilare:

```text
docs/template_report_ud08_tabelle_azure_reali.md
```

Il report deve distinguere chiaramente:

| Tipo di query | Significato |
|---|---|
| `datatable()` | esercizio controllato sulla sintassi KQL |
| tabella Azure reale | interrogazione di dati effettivamente raccolti |
| tabella assente | informazione diagnostica utile, da documentare |

## 9. Criterio di completamento

Il laboratorio è completato quando il partecipante ha prodotto almeno:

- una schermata o esportazione della discovery delle tabelle;
- una query reale riuscita, se il workspace contiene tabelle popolate;
- una nota tecnica sulle tabelle assenti o vuote;
- un confronto scritto tra query didattica con `datatable()` e query reale su tabella Azure.

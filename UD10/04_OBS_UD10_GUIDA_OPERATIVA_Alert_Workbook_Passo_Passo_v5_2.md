# 04 - UD10 Guida operativa passo passo

## Alert, Dashboard e Workbook

Questa guida serve come promemoria rapido durante l'esercitazione.

## 1. Preparazione locale

Da terminale locale o WSL, dentro `UD10`:

```bash
pwd
find . -maxdepth 3 -type d | sort
cp docs/template_monitoring_pack_ud10.md docs/report_ud10_lavoro.md
cp docs/template_alert_decision_record_ud10.md docs/alert_decision_record_lavoro.md
cp docs/template_workbook_outline_ud10.md docs/workbook_outline_lavoro.md
```

## 2. Aprire Logs nel Portale Azure

Percorso:

```text
Azure Portal
-> Log Analytics workspaces
-> selezionare il workspace UD08
-> Logs
```

Impostare un time range coerente con la query. Per query con `datatable()` il time range del portale incide poco; per tabelle reali Azure è invece fondamentale.

## 3. Eseguire query simulate

Prima eseguire una query didattica stabile:

```text
src/kql/alert/03_alert_error_rate_condition.kql
```

Controllare:

```text
Total
Errors
ErrorRate
```

Poi eseguire:

```text
src/kql/alert/04_alert_noise_threshold_review.kql
```

Usarla per ragionare sul rumore prodotto da soglie diverse.

## 4. Eseguire query per workbook

Eseguire:

```text
src/kql/workbook/01_workbook_summary_tiles_simulato.kql
src/kql/workbook/02_workbook_error_trend_timechart.kql
src/kql/workbook/03_workbook_latency_percentiles.kql
src/kql/workbook/04_workbook_top_failed_operations.kql
```

Visualizzazioni consigliate:

| Query | Visualizzazione |
|---|---|
| summary tiles | tile / tabella sintetica |
| error trend | time chart |
| latency percentiles | bar chart o tabella |
| top failed operations | tabella ordinata |

## 5. Discovery dati reali

Eseguire:

```text
src/kql/azure/01_discovery_tabelle_workspace_ud10.kql
```

Interpretazione:

| Esito | Azione |
|---|---|
| tabella presente e con righe | usarla per workbook/alert |
| tabella presente ma vuota | documentare il limite |
| tabella assente | non costruire alert su quella sorgente |
| errore schema/colonna | adattare la query alla tabella reale |

## 6. Query reali candidate

Scegliere in base alle tabelle disponibili:

| Tabella | Query |
|---|---|
| `AzureActivity` | `02_workbook_azureactivity_stati.kql`, `03_workbook_azureactivity_timechart.kql`, `04_alert_azureactivity_errori_recenti.kql` |
| `AppServiceHTTPLogs` | `05_workbook_appservice_http_status.kql`, `06_alert_appservice_5xx_recenti.kql` |
| `StorageBlobLogs` | `07_workbook_storageblob_status.kql`, `08_alert_storageblob_errori_recenti.kql` |
| `Heartbeat` | `09_workbook_vm_heartbeat.kql`, `10_alert_vm_heartbeat_assente.kql` |
| `AzureDiagnostics` | `11_fallback_azurediagnostics_errori.kql` |

## 7. Creare o progettare un Alert

Percorso portale:

```text
Monitor
-> Alerts
-> Create
-> Alert rule
```

Campi da controllare:

```text
Scope
Condition
Custom log search
Query
Measurement
Aggregation granularity
Frequency of evaluation
Threshold
Actions
Details
Severity
```

Per il laboratorio è sufficiente documentare la configurazione se non si crea realmente la regola.

## 8. Creare o progettare un Action Group

Percorso:

```text
Monitor
-> Alerts
-> Action groups
-> Create
```

Campi minimi:

```text
Nome
Resource group
Display name
Notification type
Recipient / endpoint
Tags
```

Evitare destinatari personali non necessari e notifiche ripetute non controllate.

## 9. Creare una Dashboard

Percorso:

```text
Dashboard
-> Create
-> Add tile
```

Oppure dalle query:

```text
Logs
-> Run query
-> Pin to dashboard, se disponibile
```

La dashboard deve avere pochi pannelli. Non trasformarla in un archivio di tutte le query.

## 10. Creare un Workbook

Percorso:

```text
Monitor
-> Workbooks
-> New
```

Elementi utili:

```text
Text
Parameters
Query
Visualization
Time range
```

Sequenza consigliata:

```text
Titolo e scenario
Parametro time range
Tile riepilogative
Trend temporale
Dettaglio
Note operative
```

## 11. Salvare evidenze

Salvare screenshot o output in:

```text
evidence/
```

Comandi finali:

```bash
find docs evidence -maxdepth 2 -type f | sort | tee evidence/ud10_file_list_final.txt
git status --short | tee evidence/ud10_git_status.txt
```

## 12. Checklist finale

| Controllo | OK |
|---|---|
| Query candidata per alert scelta |  |
| Soglia motivata |  |
| Finestra e frequenza indicate |  |
| Severità assegnata |  |
| Action Group progettato |  |
| Dashboard o workbook progettato |  |
| Evidenze salvate |  |
| Limiti dei dati reali indicati |  |

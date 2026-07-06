# 01 - UD10 Laboratorio guidato

## Alert, Action Group, Dashboard e Workbook

## 1. Obiettivo del laboratorio

In questo laboratorio costruiamo un percorso operativo completo:

```text
query KQL -> condizione -> soglia -> alert decision record -> dashboard/workbook -> evidenze
```

Non è obbligatorio creare notifiche reali se l'ambiente non è predisposto. È invece obbligatorio saper motivare la query candidata, la soglia e la severità.

## 2. Prerequisiti

Devono essere disponibili:

- repository locale del corso;
- cartella `UD10/`;
- accesso al Portale Azure;
- Log Analytics Workspace creato in UD08;
- query KQL di UD09 già eseguite almeno una volta;
- risorse Azure delle UD precedenti, se ancora presenti.

## 3. Dove lavoriamo

| Attività | Ambiente |
|---|---|
| Esecuzione query KQL | Azure Portal -> Log Analytics Workspace -> Logs |
| Salvataggio report | repository locale / WSL / VS Code |
| Screenshot | `evidence/` |
| Template | `docs/` |
| Verifiche rapide Azure | Portale Azure o Cloud Shell |

Cloud Shell non coincide con la cartella locale del repository. Le evidenze finali vanno salvate nel repository locale.

## 4. Preparazione cartelle

Aprire il terminale nella cartella `UD10` ed eseguire:

```bash
pwd
find . -maxdepth 3 -type d | sort
```

Verificare che esistano almeno:

```text
docs/
evidence/
src/kql/alert/
src/kql/workbook/
src/kql/azure/
```

Creare una copia del template guidato:

```bash
cp docs/template_monitoring_pack_ud10.md docs/report_ud10_guidato.md
cp docs/template_alert_decision_record_ud10.md docs/alert_decision_record_guidato.md
```

## 5. Esecuzione query candidate per alert

Aprire nel portale Azure:

```text
Log Analytics Workspace -> Logs
```

Eseguire le query in questa sequenza.

| Ordine | Query | Scopo |
|---:|---|---|
| 1 | `src/kql/alert/01_dataset_alert_failed_operations_simulato.kql` | capire il dataset e i campi |
| 2 | `src/kql/alert/02_alert_failed_operations_condition.kql` | individuare una condizione di fallimento |
| 3 | `src/kql/alert/03_alert_error_rate_condition.kql` | calcolare error rate candidato per alert |
| 4 | `src/kql/alert/04_alert_noise_threshold_review.kql` | confrontare soglie e rischio rumore |

Per ogni query annotare:

```text
Che cosa misura?
Quale condizione produce?
La query è adatta a un alert o a un workbook?
Quale rischio di falso positivo vedo?
```

## 6. Analisi della prima query candidata

Usare la query:

```text
src/kql/alert/02_alert_failed_operations_condition.kql
```

Interpretazione attesa:

- aggrega operazioni fallite per risorsa;
- calcola totale e percentuale di fallimento;
- restituisce solo risorse con almeno 3 fallimenti;
- può essere una candidata per alert perché produce una condizione sintetica.

Nel file `docs/alert_decision_record_guidato.md` compilare:

```text
Scenario monitorato
Query scelta
Soglia proposta
Finestra temporale
Frequenza di valutazione
Severità
Action Group previsto
Rischio di falso positivo
Prima azione di verifica
```

## 7. Analisi della seconda query candidata

Usare:

```text
src/kql/alert/03_alert_error_rate_condition.kql
```

Questa query è migliore di “almeno 1 errore” perché include:

- volume minimo;
- conteggio totale;
- conteggio errori;
- percentuale di errore;
- soglia percentuale.

Nel report scrivere perché una soglia percentuale con volume minimo è più robusta di una soglia basata su un singolo evento.

## 8. Confronto soglie e rumore

Eseguire:

```text
src/kql/alert/04_alert_noise_threshold_review.kql
```

La query mostra come cambiano le decisioni al variare della soglia.

Domande da rispondere nel report:

```text
Quale soglia scatterebbe sempre?
Quale soglia sembra troppo permissiva?
Quale soglia sembra troppo severa?
Quale soglia proporresti in un ambiente didattico?
Quali dati storici servirebbero per scegliere meglio?
```

## 9. Query per dashboard e workbook

Eseguire le query in `src/kql/workbook/`.

| Query | Uso prevalente |
|---|---|
| `01_workbook_summary_tiles_simulato.kql` | tile riepilogative |
| `02_workbook_error_trend_timechart.kql` | grafico temporale errori |
| `03_workbook_latency_percentiles.kql` | latenza media e percentili |
| `04_workbook_top_failed_operations.kql` | dettaglio per operazione e risorsa |

Per ogni query decidere se è più adatta a:

```text
alert
dashboard
workbook
runbook investigativo
```

## 10. Bozza dashboard

Disegnare una dashboard minima con 4 pannelli:

| Pannello | Query sorgente | Domanda operativa |
|---|---|---|
| Stato sintetico | summary tiles | il servizio sembra stabile? |
| Trend errori | error trend | gli errori aumentano? |
| Latenza p95/p99 | latency percentiles | ci sono code lente? |
| Top failure | top failed operations | dove concentro l'indagine? |

Compilare la sezione corrispondente in `docs/report_ud10_guidato.md`.

## 11. Bozza workbook

Creare una struttura logica del workbook usando:

```bash
cp docs/template_workbook_outline_ud10.md docs/workbook_outline_guidato.md
```

Il workbook deve includere:

```text
1. Descrizione scenario
2. Parametri di analisi
3. Sintesi
4. Trend temporale
5. Dettaglio tecnico
6. Interpretazione e limiti
```

Il workbook non deve essere una copia della dashboard. Deve guidare una diagnosi.

## 12. Action Group: progettazione

Documentare l'Action Group previsto.

Campi minimi:

| Campo | Esempio |
|---|---|
| Nome | `ag-obs-ud10-training` |
| Canale | email o notifica simulata |
| Destinatario | gruppo operativo del laboratorio |
| Messaggio | indicare scenario, severità, prima verifica |
| Note | non usare destinatari personali non necessari |

Nel laboratorio può bastare la progettazione. La creazione reale va fatta solo se coerente con l'ambiente e con le regole di costo/notifica.

## 13. Orientamento nel Portale Azure

Percorsi utili:

```text
Monitor -> Alerts -> Alert rules
Monitor -> Alerts -> Action groups
Monitor -> Workbooks
Log Analytics Workspace -> Logs
Dashboard -> Create dashboard
```

Campi da osservare in una regola di alert log-based:

```text
Scope
Condition
Query
Measurement
Aggregation granularity
Frequency of evaluation
Threshold
Actions
Details
Severity
```

## 14. Evidenze finali

Salvare in `evidence/` almeno:

```text
screenshot_query_alert_candidate.png
screenshot_query_workbook_trend.png
screenshot_portale_alert_fields.png oppure nota descrittiva
screenshot_workbook_outline.png oppure schema testuale
ud10_file_list_final.txt
ud10_git_status.txt
```

Comandi utili:

```bash
find docs evidence -maxdepth 2 -type f | sort | tee evidence/ud10_file_list_final.txt
git status --short | tee evidence/ud10_git_status.txt
```

## 15. Chiusura del laboratorio guidato

Nel report devono comparire almeno queste frasi tecniche, completate in modo specifico:

```text
La query scelta misura ...
La soglia scelta è ... perché ...
La finestra di valutazione proposta è ... perché ...
Il rischio principale di falso positivo è ...
L'Action Group deve comunicare ...
La dashboard risponde rapidamente a ...
Il workbook serve ad approfondire ...
```

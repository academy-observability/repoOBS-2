# 00 - UD09 Concetti: KQL per troubleshooting e aggregazioni

## 1. Posizione della UD09 nel percorso

Nella UD08 abbiamo imparato a usare Log Analytics Workspace e KQL di base. Abbiamo visto che una query può usare dati simulati con `datatable()` oppure tabelle Azure reali popolate tramite Diagnostic settings, Activity Log o Azure Monitor Agent.

La UD09 fa un passo ulteriore: usa KQL per rispondere a domande diagnostiche.

Domanda guida:

```text
Il sistema ha avuto un problema? Dove, quando, quanto spesso e con quale impatto?
```

## 2. Dal record alla diagnosi

Una query base mostra righe. Una query diagnostica trasforma molte righe in indicatori utili.

| Livello | Esempio | Utilità |
|---|---|---|
| Record singolo | una richiesta HTTP con status 500 | prova puntuale |
| Filtro | tutte le richieste fallite | riduzione del rumore |
| Aggregazione | errori per risorsa | confronto |
| Trend | errori ogni 15 minuti | individuazione finestra critica |
| Indicatore | error rate, P95, conteggio errori | base per decisione operativa |

## 3. Comandi KQL centrali

| Operatore/funzione | Uso diagnostico |
|---|---|
| `where` | riduce il dataset a ciò che conta |
| `project` | mantiene solo le colonne utili |
| `extend` | calcola colonne derivate |
| `summarize` | trasforma record in indicatori |
| `count()` | conta i record |
| `countif()` | conta solo i record che rispettano una condizione |
| `avg()`, `min()`, `max()` | calcolano statistiche semplici |
| `percentile()` | misura code e picchi non visibili dalla media |
| `bin()` | raggruppa il tempo in finestre regolari |
| `sort by` | ordina il risultato per evidenziare priorità |

## 4. Errori assoluti ed error rate

Il numero di errori non basta. Una risorsa con molto traffico può avere più errori assoluti di una risorsa quasi inutilizzata, ma un tasso di errore minore.

Esempio:

```kql
OperationEvents
| summarize Totale=count(), Errori=countif(Result == "Failed") by Resource
| extend ErrorRate = round(100.0 * Errori / Totale, 2)
| sort by ErrorRate desc
```

Interpretazione:

```text
Totale = volume osservato
Errori = fallimenti osservati
ErrorRate = percentuale di fallimenti sul volume totale
```

## 5. Trend temporale con `bin()`

`bin()` consente di vedere quando si concentra il problema.

```kql
OperationEvents
| where Result == "Failed"
| summarize Errori=count() by bin(TimeGenerated, 15m)
| sort by TimeGenerated asc
```

La finestra scelta cambia la lettura:

| Finestra | Lettura |
|---|---|
| `1m` | molto dettaglio, più rumore |
| `5m` | utile per test rapidi |
| `15m` | buon compromesso didattico |
| `1h` | visione sintetica |

## 6. Media, massimo e percentili

Per la latenza la media può nascondere picchi importanti. Per questo usiamo anche P95 o P99.

```kql
OperationEvents
| summarize Media=avg(DurationMs), P95=percentile(DurationMs, 95), Max=max(DurationMs) by Operation
```

| Indicatore | Significato |
|---|---|
| Media | comportamento medio |
| Max | peggiore valore osservato |
| P95 | soglia sotto cui cade circa il 95% dei valori |
| P99 | evidenzia code lunghe e casi estremi |

## 7. Query candidata per alert

Una query candidata per alert deve essere stabile, leggibile e collegata a una soglia.

Una buona query da alert dichiara:

```text
finestra temporale
condizione osservata
soglia
impatto operativo
```

Esempio:

```kql
OperationEvents
| where TimeGenerated > ago(30m)
| where Operation == "/api/payments"
| summarize Totale=count(), Errori=countif(Result == "Failed"), P95Ms=percentile(DurationMs, 95)
| extend ErrorRate = round(100.0 * Errori / Totale, 2)
| where ErrorRate >= 20 or P95Ms >= 2000
```

Questa query restituisce righe solo quando la condizione è superata. Nella UD10 verrà trasformata in alert rule.

## 8. Tabelle reali Azure

Il metodo si applica anche alle tabelle reali viste in UD08.

| Tabella | Uso tipico |
|---|---|
| `AzureActivity` | operazioni amministrative, create/update/delete, errori del piano di controllo |
| `AppServiceHTTPLogs` | richieste HTTP della Web App |
| `StorageBlobLogs` | operazioni su Blob Storage |
| `AzureMetrics` | metriche esportate nel workspace |
| `Heartbeat`, `Perf` | segnali VM raccolti con Azure Monitor Agent e DCR |
| `AzureDiagnostics` | tabella legacy/fallback per alcuni resource log |

## 9. Risultato vuoto e tabella assente

Nel troubleshooting KQL bisogna distinguere tre casi:

| Caso | Significato probabile | Azione |
|---|---|---|
| Query valida, zero righe | nessun dato nella finestra selezionata | allargare il time range o generare traffico |
| Errore “table not found” | tabella non presente nel LAW | verificare Diagnostic settings o DCR |
| Dati presenti ma non coerenti | filtro troppo stretto o colonna sbagliata | controllare schema e colonne |

Questa distinzione è fondamentale: un workspace reale non garantisce automaticamente dati in ogni tabella.

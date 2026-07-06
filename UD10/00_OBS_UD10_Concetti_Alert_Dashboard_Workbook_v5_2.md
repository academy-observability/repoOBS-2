# 00 - UD10 Concetti

## Alert, Action Group, Dashboard e Workbook

## 1. Posizione della UD10 nel percorso

La UD10 trasforma le query KQL in strumenti operativi.

```text
UD08 -> creiamo il Log Analytics Workspace e impariamo KQL base
UD09 -> usiamo KQL per troubleshooting, aggregazioni e runbook investigativi
UD10 -> scegliamo cosa visualizzare, quando notificare e come documentare il monitoraggio
```

Il passaggio chiave è questo:

```text
query interessante -> segnale interpretato -> soglia -> alert/dashboard/workbook -> decisione operativa
```

## 2. Osservabilità e monitoraggio non sono la stessa cosa

L'osservabilità riguarda la capacità di capire lo stato interno di un sistema partendo dai segnali prodotti: log, metriche, tracce, eventi, heartbeat.

Il monitoraggio è l'uso operativo di quei segnali: pannelli, soglie, notifiche, runbook, escalation e decisioni.

In UD10 non ci limitiamo a “vedere dati”: decidiamo quali dati meritano attenzione operativa.

## 3. Alert

Un alert è una regola che valuta periodicamente una condizione e genera una notifica o un evento operativo quando quella condizione è vera.

Elementi fondamentali:

| Elemento | Domanda a cui risponde |
|---|---|
| Scope | Quale risorsa o workspace sto monitorando? |
| Signal / query | Quale segnale sto valutando? |
| Evaluation period | Su quale finestra temporale controllo i dati? |
| Frequency | Ogni quanto controllo la condizione? |
| Threshold | Quale valore fa scattare l'alert? |
| Severity | Quanto è grave il problema? |
| Action Group | Chi o cosa viene attivato? |
| Description | Cosa deve capire chi riceve l'alert? |

Un alert non deve nascere da una query casuale. Deve nascere da un rischio operativo.

## 4. Query candidata per alert

Una query candidata per alert deve avere queste caratteristiche:

- finestra temporale esplicita;
- risultato sintetico;
- condizione misurabile;
- basso rischio di rumore;
- legame con un'azione concreta;
- spiegazione della soglia.

Esempio concettuale:

```kql
AppRequests
| where TimeGenerated > ago(15m)
| summarize Total=count(), Errors=countif(Success == false)
| extend ErrorRate = round(todouble(Errors) / todouble(Total) * 100, 2)
| where Total >= 20 and ErrorRate >= 10
```

Questa query non dice solo “ci sono errori”. Dice: negli ultimi 15 minuti, con almeno 20 richieste, l'error rate supera il 10%.

## 5. Soglia

La soglia separa il comportamento accettabile dal comportamento che richiede attenzione.

Esempi di soglia debole:

```text
almeno 1 errore
latenza > 200 ms
qualunque operazione fallita
```

Esempi più solidi:

```text
error rate > 10% con almeno 20 richieste nella finestra
p95 di latenza > 1000 ms per 15 minuti
almeno 3 operazioni fallite sulla stessa risorsa in 30 minuti
assenza di heartbeat VM per oltre 15 minuti
```

La soglia deve ridurre il rumore senza nascondere problemi reali.

## 6. Finestra di valutazione e frequenza

Sono due concetti diversi.

| Concetto | Significato | Esempio |
|---|---|---|
| Finestra di valutazione | Periodo di dati analizzato | ultimi 15 minuti |
| Frequenza di valutazione | Ogni quanto la regola viene controllata | ogni 5 minuti |

Con una finestra di 15 minuti e frequenza di 5 minuti, l'alert viene valutato ogni 5 minuti guardando i 15 minuti precedenti.

## 7. Severità

La severità esprime l'impatto operativo, non solo il valore numerico della metrica.

| Severità | Uso nel laboratorio |
|---|---|
| Sev 0 | servizio indisponibile o impatto critico |
| Sev 1 | degrado importante e visibile |
| Sev 2 | problema significativo ma circoscritto |
| Sev 3 | anomalia da investigare |
| Sev 4 | informazione o segnale debole |

Un errore amministrativo su una risorsa non critica può essere Sev 3. La stessa condizione su una risorsa centrale può diventare Sev 1.

## 8. Action Group

Un Action Group definisce cosa accade quando un alert scatta.

Possibili azioni:

- email;
- SMS o push, se configurati;
- webhook;
- automazione;
- integrazione con sistemi ITSM;
- funzione serverless.

Nel laboratorio l'obiettivo non è generare notifiche reali a tutti i costi, ma progettare un Action Group coerente con lo scenario.

## 9. Dashboard

Una dashboard è una vista sintetica per capire rapidamente lo stato del sistema.

Domande tipiche:

```text
Il servizio risponde?
Gli errori stanno aumentando?
La latenza è stabile?
Quale risorsa ha più segnali anomali?
```

Una dashboard efficace ha pochi pannelli, leggibili e orientati alla decisione.

## 10. Workbook

Un Workbook è più analitico di una dashboard. Serve a guidare l'indagine.

Struttura consigliata:

```text
1. Titolo e scenario
2. Parametri: time range, risorsa, servizio
3. Sintesi numerica
4. Trend temporale
5. Dettaglio per risorsa/operazione
6. Note operative e limiti dei dati
```

La dashboard risponde “come sta andando?”. Il workbook aiuta a rispondere “perché sta accadendo?”.

## 11. Monitoring Pack

Un monitoring pack minimo contiene:

```text
query candidate
+ alert decision record
+ action group progettato
+ dashboard/workbook
+ runbook minimo
+ evidenze
```

Il valore sta nella coerenza tra segnale, soglia, severità e azione.

## 12. Falsi positivi e alert fatigue

Un falso positivo è un alert che scatta senza richiedere una vera azione.

La conseguenza è alert fatigue: troppe notifiche poco utili fanno perdere fiducia nel sistema di monitoraggio.

Riduciamo il rumore con:

- volume minimo;
- finestre temporali adeguate;
- percentili invece di singoli outlier;
- severità differenziate;
- descrizioni operative chiare;
- runbook minimo collegato all'alert.

## 13. Tabelle reali e dati simulati

In UD10 usiamo due tipi di dati.

| Tipo | Perché lo usiamo |
|---|---|
| Dataset simulato con `datatable()` | Garantisce esercizi ripetibili anche se il workspace è vuoto |
| Tabelle reali Azure | Permettono monitoring pack aderenti all'ambiente creato nelle UD precedenti |

Una query simulata serve per imparare la logica. Una query su dati reali serve per progettare un monitoraggio credibile.

## 14. Tabelle reali utili, quando disponibili

| Tabella | Uso possibile |
|---|---|
| `AzureActivity` | operazioni amministrative, errori di gestione risorse |
| `AzureMetrics` | metriche inviate al workspace |
| `AppServiceHTTPLogs` | traffico HTTP e status code App Service |
| `StorageBlobLogs` | operazioni su Blob Storage |
| `Heartbeat` | stato invio dati da VM con Azure Monitor Agent / DCR |
| `Perf` | performance VM, se raccolta configurata |
| `AzureDiagnostics` | fallback per servizi che scrivono ancora in questa tabella |

Una tabella può non esistere o essere vuota. In quel caso non si forza l'alert: si documenta il limite.

## 15. Regola di qualità UD10

Un buon alert risponde a questa sequenza:

```text
Che rischio voglio intercettare?
Quale segnale lo rappresenta?
Quale query lo misura?
Quale soglia è ragionevole?
Quale severità assegno?
Chi o cosa deve reagire?
Quale dashboard/workbook aiuta a capire il contesto?
```

Una configurazione tecnicamente corretta ma priva di decisione operativa non è sufficiente.

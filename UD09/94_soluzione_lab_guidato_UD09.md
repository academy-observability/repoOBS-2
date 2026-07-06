# Soluzione attesa - UD09 Lab guidato
## KQL troubleshooting e aggregazioni

> Scopo del documento: fornire una traccia di svolgimento completa ma sintetica del laboratorio guidato UD09.  
> Il partecipante non deve necessariamente produrre testi identici, ma deve arrivare agli stessi risultati concettuali: usare KQL per trasformare record grezzi in indicatori diagnostici.

---

## 1. Dati generali del laboratorio

| Voce | Valore atteso |
|---|---|
| Workspace LAW | Workspace usato in UD08 |
| Modalità esecuzione | Azure Portal → Log Analytics Workspace → Logs |
| Dataset principale | Query `datatable()` in `src/kql/local/` |
| Obiettivo | Identificare componente problematico, finestra temporale critica e query candidata per alert UD10 |

---

## 2. Query 01 - Dataset operazioni

### Query usata

```text
src/kql/local/01_dataset_operazioni.kql
```

### Risultato atteso

La query restituisce un dataset simulato di eventi applicativi con colonne simili a queste:

```text
TimeGenerated
Service
Resource
Operation
Result
StatusCode
DurationMs
RequestId
Region
Severity
```

### Interpretazione attesa

Il dataset rappresenta richieste applicative verso più componenti:

```text
api-gateway-01
catalog-api-01
orders-api-01
payments-api-01
```

Sono presenti richieste riuscite e richieste fallite. Le colonne più utili per la diagnosi sono:

```text
Resource
Operation
Result
StatusCode
DurationMs
TimeGenerated
Severity
```

### Evidenza attesa

```text
evidence/ud09_01_dataset.png
```

---

## 3. Query 02 - Error rate per risorsa

### Query usata

```text
src/kql/local/02_error_rate_per_risorsa.kql
```

### Risultato atteso indicativo

| Resource | Totale | Errori | ErrorRate | Latenza media indicativa | Latenza massima |
|---|---:|---:|---:|---:|---:|
| payments-api-01 | 10 | 6 | 60% | circa 1836 ms | 3300 ms |
| orders-api-01 | 6 | 2 | 33,33% | circa 627 ms | 1480 ms |
| api-gateway-01 | 4 | 1 | 25% | circa 427 ms | 1650 ms |
| catalog-api-01 | 4 | 0 | 0% | circa 104 ms | 115 ms |

### Interpretazione attesa

La risorsa più critica è:

```text
payments-api-01
```

Motivazione:

```text
payments-api-01 ha il maggior numero di errori, il tasso di errore più alto e la latenza massima più elevata.
```

Nota importante:

```text
api-gateway-01 ha un ErrorRate del 25%, ma su un volume molto basso: 1 errore su 4 eventi. Per questo non va interpretato come problema principale senza ulteriore verifica.
```

### Evidenza attesa

```text
evidence/ud09_02_error_rate.png
```

---

## 4. Query 03 - Trend temporale errori con `bin(15m)`

### Query usata

```text
src/kql/local/03_trend_temporale_errori_bin_15m.kql
```

### Risultato atteso

La query raggruppa gli eventi in finestre temporali da 15 minuti.

Il risultato deve mostrare una o più finestre con crescita degli errori. La finestra più critica è quella in cui si concentrano più errori sul servizio pagamenti.

Indicazione attesa:

```text
La concentrazione anomala degli errori si colloca nella parte centrale del dataset, quando iniziano a comparire più fallimenti su /api/payments e /api/orders.
```

### Interpretazione attesa

Il problema non è distribuito uniformemente su tutto il periodo osservato. Esiste una finestra temporale in cui errori e latenza aumentano.

Conclusione corretta:

```text
Il trend temporale conferma che il problema è concentrato in una finestra specifica e non è solo rumore isolato.
```

### Evidenza attesa

```text
evidence/ud09_03_trend_errori.png
```

---

## 5. Query 04 - Latenza e percentili

### Query usata

```text
src/kql/local/04_latenza_percentili_p95_p99.kql
```

### Risultato atteso

La query calcola:

```text
Richieste
LatenzaMediaMs
LatenzaMassimaMs
P95Ms
P99Ms
```

per ogni `Operation`.

### Interpretazione attesa

L'operazione più critica è:

```text
/api/payments
```

Motivazione:

```text
/api/payments mostra valori di latenza molto più alti rispetto a /health, /api/catalog e /api/orders.
```

La media da sola non è sufficiente perché può nascondere picchi. Il P95 è più adatto per capire se una quota significativa delle richieste ha tempi elevati.

Conclusione corretta:

```text
La latenza alta rafforza l'ipotesi che il problema principale riguardi il servizio pagamenti.
```

### Evidenza attesa

```text
evidence/ud09_04_percentili.png
```

---

## 6. Query 05 - Top operazioni lente

### Query usata

```text
src/kql/local/05_top_operazioni_lente.kql
```

### Risultato atteso

Le prime righe ordinate per `DurationMs desc` devono mostrare soprattutto richieste verso:

```text
/api/payments
payments-api-01
```

con durate elevate, per esempio valori nell'ordine di:

```text
3300 ms
3100 ms
2950 ms
2890 ms
2320 ms
```

### Interpretazione attesa

Le operazioni più lente non sono distribuite casualmente: sono concentrate sul pagamento.

Conclusione corretta:

```text
La top 10 delle richieste lente conferma che /api/payments è il punto più critico del dataset.
```

### Evidenza attesa

```text
evidence/ud09_05_top_lente.png
```

---

## 7. Query 06 - Finestra incidente candidata

### Query usata

```text
src/kql/local/06_finestra_incidente_candidata.kql
```

### Risultato atteso

La query combina:

```text
Eventi
Errori
LatenzaMediaMs
P95Ms
ErrorRate
```

per finestra temporale.

### Interpretazione attesa

La finestra candidata di incidente è quella con:

```text
ErrorRate elevato
più errori concentrati
P95 alto
```

Conclusione sintetica attesa:

```text
Il dataset mostra un'anomalia concentrata nella fase centrale della finestra osservata. Il servizio più coinvolto è payments-api-01 e l'operazione più critica è /api/payments.
```

### Evidenza attesa

```text
evidence/ud09_06_finestra_incidente.png
```

---

## 8. Query 07 - Query candidata per alert UD10

### Query usata

```text
src/kql/local/07_query_alert_candidata.kql
```

### Query candidata

```kql
// Query candidata per alert UD10
// Scenario: troppi errori o latenza elevata sul servizio pagamenti

let BaseTime = now() - 2h;
let OperationEvents = datatable(
    OffsetMin:int,
    Service:string,
    Resource:string,
    Operation:string,
    Result:string,
    StatusCode:int,
    DurationMs:int,
    RequestId:string,
    Region:string,
    Severity:string
)
[
    0,   "academy-shop", "api-gateway-01",  "/health",       "Success", 200,   18, "req-0001", "westeurope", "Info",
    5,   "academy-shop", "catalog-api-01",  "/api/catalog",  "Success", 200,   95, "req-0002", "westeurope", "Info",
    10,  "academy-shop", "orders-api-01",   "/api/orders",   "Success", 201,  180, "req-0003", "westeurope", "Info",
    15,  "academy-shop", "payments-api-01", "/api/payments", "Success", 200,  240, "req-0004", "westeurope", "Info",
    20,  "academy-shop", "catalog-api-01",  "/api/catalog",  "Success", 200,  105, "req-0005", "westeurope", "Info",
    25,  "academy-shop", "orders-api-01",   "/api/orders",   "Success", 201,  230, "req-0006", "westeurope", "Info",
    30,  "academy-shop", "payments-api-01", "/api/payments", "Success", 200,  280, "req-0007", "westeurope", "Info",
    35,  "academy-shop", "payments-api-01", "/api/payments", "Failed",  500, 1850, "req-0008", "westeurope", "Error",
    40,  "academy-shop", "orders-api-01",   "/api/orders",   "Success", 201,  260, "req-0009", "westeurope", "Info",
    45,  "academy-shop", "payments-api-01", "/api/payments", "Failed",  502, 2320, "req-0010", "westeurope", "Error",
    50,  "academy-shop", "payments-api-01", "/api/payments", "Failed",  504, 3100, "req-0011", "westeurope", "Error",
    55,  "academy-shop", "orders-api-01",   "/api/orders",   "Failed",  500, 1250, "req-0012", "westeurope", "Error",
    60,  "academy-shop", "api-gateway-01",  "/health",       "Success", 200,   21, "req-0013", "westeurope", "Info",
    65,  "academy-shop", "payments-api-01", "/api/payments", "Failed",  502, 2890, "req-0014", "westeurope", "Error",
    70,  "academy-shop", "payments-api-01", "/api/payments", "Failed",  500, 3300, "req-0015", "westeurope", "Error",
    75,  "academy-shop", "orders-api-01",   "/api/orders",   "Failed",  500, 1480, "req-0016", "westeurope", "Error",
    80,  "academy-shop", "catalog-api-01",  "/api/catalog",  "Success", 200,  115, "req-0017", "westeurope", "Info",
    85,  "academy-shop", "payments-api-01", "/api/payments", "Success", 200,  820, "req-0018", "westeurope", "Warning",
    90,  "academy-shop", "orders-api-01",   "/api/orders",   "Success", 201,  360, "req-0019", "westeurope", "Info",
    95,  "academy-shop", "payments-api-01", "/api/payments", "Failed",  504, 2950, "req-0020", "westeurope", "Error",
    100, "academy-shop", "api-gateway-01",  "/api/payments", "Failed",  502, 1650, "req-0021", "westeurope", "Error",
    105, "academy-shop", "payments-api-01", "/api/payments", "Success", 200,  610, "req-0022", "westeurope", "Warning",
    110, "academy-shop", "catalog-api-01",  "/api/catalog",  "Success", 200,  100, "req-0023", "westeurope", "Info",
    115, "academy-shop", "api-gateway-01",  "/health",       "Success", 200,   20, "req-0024", "westeurope", "Info"
];

OperationEvents
| extend TimeGenerated = BaseTime + OffsetMin * 1m
| where TimeGenerated > ago(2h)
| where Operation == "/api/payments"
| summarize
    Totale = count(),
    Errori = countif(Result == "Failed"),
    P95Ms = percentile(DurationMs, 95)
| extend ErrorRate = iff(Totale == 0, 0.0, round(100.0 * Errori / Totale, 2))
| where ErrorRate >= 20 or P95Ms >= 2000
```

### Risultato atteso

La query deve restituire una riga, perché la condizione è superata.

Valori attesi indicativi:

```text
Totale richieste /api/payments: 11
Errori: 7
ErrorRate: circa 63,64%
P95Ms: valore superiore a 2000 ms
```

### Soglia proposta

```text
ErrorRate >= 20%
oppure
P95Ms >= 2000 ms
```

### Finestra temporale

```text
Dataset simulato: ultime 2 ore.
UD10 su dati reali: finestra consigliata 15 o 30 minuti.
```

### Motivazione operativa

```text
/api/payments rappresenta una funzionalità critica. Un tasso elevato di errori o una latenza P95 superiore a 2 secondi può indicare un degrado percepibile dagli utenti.
```

### Uso previsto in UD10

```text
Creare una Log Alert Rule con condizione: numero risultati > 0.
```

---

## 9. Conclusione finale del laboratorio guidato

Soluzione sintetica attesa dal partecipante:

```text
Dalle query UD09 emerge che il componente più problematico è payments-api-01, in particolare l'operazione /api/payments.
La risorsa mostra errori frequenti, error rate elevato e latenze alte.
Il problema è concentrato in alcune finestre temporali e non sembra riguardare in modo uniforme tutti i componenti.
La query candidata per UD10 controlla ErrorRate e P95Ms su /api/payments e restituisce una riga solo quando almeno una soglia è superata.
```

---

## 10. Checklist di consegna

Il partecipante deve consegnare almeno:

```text
docs/report_ud09_guidato.md compilato
evidence/ud09_01_dataset.png
evidence/ud09_02_error_rate.png
evidence/ud09_03_trend_errori.png
evidence/ud09_04_percentili.png
evidence/ud09_05_top_lente.png
evidence/ud09_06_finestra_incidente.png
query candidata per alert documentata
commit finale
```

Commit suggerito:

```bash
git add docs/report_ud09_guidato.md evidence/
git commit -m "UD09 guided KQL troubleshooting solution"
```

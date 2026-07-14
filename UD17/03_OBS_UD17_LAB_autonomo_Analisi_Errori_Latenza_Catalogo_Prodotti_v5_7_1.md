# OBS UD17 - Laboratorio autonomo
# Analisi di lentezza ed errore controllato sul Catalogo prodotti

## Scenario

Il cliente segnala che il Catalogo prodotti a volte è lento e a volte restituisce errore. Non dobbiamo modificare subito il codice. Prima dobbiamo raccogliere evidenze e produrre una spiegazione tecnica.

## Obiettivo

Dimostrare, con dati Azure, che sappiamo distinguere:

- richiesta normale;
- richiesta lenta;
- richiesta in errore;
- problema frontend;
- problema backend;
- problema di collegamento FE → BE.

## Vincoli

Non creare nuove risorse Azure. Usare le risorse già presenti:

- frontend ACA;
- backend ACA;
- Application Insights;
- Log Analytics;
- pipeline/release products già completata.

## Task 1 - Generare tre request id

```bash
RID_OK="ud17-auto-ok-$(date +%s)"
RID_SLOW="ud17-auto-slow-$(date +%s)"
RID_ERR="ud17-auto-err-$(date +%s)"
```

## Task 2 - Generare traffico mirato

```bash
curl -i -H "X-Request-Id: $RID_OK" "$FRONTEND_URL/products"
curl -i -H "X-Request-Id: $RID_SLOW" "$FRONTEND_URL/products/slow"
curl -i -H "X-Request-Id: $RID_ERR" "$FRONTEND_URL/products/error"
```

Annotare gli status code.

## Task 3 - Trovare le request in Application Insights

Usare KQL per trovare gli endpoint:

```kql
AppRequests
| where TimeGenerated > ago(2h)
| where Url has "/products"
| project TimeGenerated, AppRoleName, Name, Url, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

## Task 4 - Trovare le dependency FE → BE

```kql
AppDependencies
| where TimeGenerated > ago(2h)
| where Data has "/api/products" or Name has "/api/products"
| project TimeGenerated, AppRoleName, Name, Target, Data, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

## Task 5 - Trovare i log JSON tramite request_id

Sostituire il valore:

```kql
let rid = "INCOLLA_REQUEST_ID";
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(2h)
| where Log_s has rid
| extend j=parse_json(Log_s)
| project TimeGenerated, ContainerAppName_s, service=tostring(j.service), path=tostring(j.path), status=toint(j.status), latency_ms=todouble(j.latency_ms), request_id=tostring(j.request_id), trace_id=tostring(j.trace_id)
| order by TimeGenerated asc
```

## Task 6 - Compilare tabella di diagnosi

| Caso | Endpoint | Status | Evidenza request | Evidenza dependency | Evidenza log | Interpretazione |
|---|---|---:|---|---|---|---|
| Normale | `/products` |  |  |  |  |  |
| Lento | `/products/slow` |  |  |  |  |  |
| Errore | `/products/error` |  |  |  |  |  |  |

## Task 7 - Decision record autonomo

Compilare:

```text
Osservazione:
Evidenza principale:
Evidenza secondaria:
Ipotesi:
Verifica:
Decisione consigliata:
Limite dell'analisi:
```

## Criterio di completamento

Il laboratorio è completo se riesci a dimostrare almeno una di queste conclusioni:

1. la lentezza nasce nel backend;
2. l'errore è un errore controllato sul percorso products;
3. il frontend è vivo ma dipende correttamente dal backend;
4. request e log container raccontano la stessa storia.

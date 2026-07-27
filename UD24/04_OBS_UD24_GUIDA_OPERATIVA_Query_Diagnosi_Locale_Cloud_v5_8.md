# OBS UD24 — Guida operativa
# Query e diagnosi locale/cloud

## 0. Scopo

Questa guida raccoglie i comandi e le query più utili per investigare i problemi del Catalogo prodotti. Non sostituisce il ragionamento: serve a evitare dispersione quando si cercano segnali.

## 1. Verifiche HTTP

```bash
curl -i "$FRONTEND_URL/health"
curl -i "$FRONTEND_URL/ready"
curl -i "$FRONTEND_URL/products"
curl -i "$FRONTEND_URL/products/slow"
curl -i "$FRONTEND_URL/products/error"
```

Interpretazione:

| Endpoint | Se fallisce |
|---|---|
| `/health` | il frontend potrebbe non essere sano |
| `/ready` | il frontend potrebbe non raggiungere il backend |
| `/products` | problema nel flusso normale catalogo |
| `/products/slow` | latenza controllata o timeout |
| `/products/error` | errore applicativo controllato |

## 2. PromQL locali

### Target up/down

```promql
up
```

### Request rate per path/status

```promql
sum(rate(http_requests_total[2m])) by (service, path, status)
```

### Error rate 5xx

```promql
sum(rate(http_requests_total{status=~"5.."}[2m])) by (service, path, status)
```

### Latenza media

```promql
sum(rate(http_request_duration_seconds_sum[5m])) by (service, path)
/
sum(rate(http_request_duration_seconds_count[5m])) by (service, path)
```

### p95 latenza

```promql
histogram_quantile(
  0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service, path)
)
```

Se le metriche hanno nomi diversi, apri `/metrics` sul servizio interessato e adatta la query.

## 3. KQL cloud

### Richieste per endpoint

```kql
AppRequests
| where TimeGenerated > ago(1h)
| where Url has "/products" or Name has "products"
| summarize richieste=count(), durata_media_ms=avg(DurationMs), p95_ms=percentile(DurationMs, 95) by bin(TimeGenerated, 5m), Name, ResultCode
| order by TimeGenerated asc
```

### Errori 5xx

```kql
AppRequests
| where TimeGenerated > ago(1h)
| where ResultCode startswith "5"
| project TimeGenerated, Name, Url, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

### Dipendenze frontend → backend

```kql
AppDependencies
| where TimeGenerated > ago(1h)
| where Target has "backend" or Name has "products"
| project TimeGenerated, Name, Target, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

### Eccezioni

```kql
AppExceptions
| where TimeGenerated > ago(1h)
| project TimeGenerated, AppRoleName, Type, Message, OperationId
| order by TimeGenerated desc
```

### Trace applicativi

```kql
AppTraces
| where TimeGenerated > ago(1h)
| where Message has "request_id" or Message has "products"
| project TimeGenerated, AppRoleName, SeverityLevel, Message, OperationId
| order by TimeGenerated desc
```

### Log container ACA

```kql
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(1h)
| where Log_s has "products" or Log_s has "request_id" or Log_s has "ERROR"
| project TimeGenerated, ContainerAppName_s, RevisionName_s, Log_s
| order by TimeGenerated desc
```

## 4. Controllo revisioni ACA

```bash
az containerapp revision list \
  --resource-group "$RESOURCE_GROUP" \
  --name "$FRONTEND_APP" \
  -o table

az containerapp revision list \
  --resource-group "$RESOURCE_GROUP" \
  --name "$BACKEND_APP" \
  -o table
```

Se una nuova release ha introdotto il problema, le revisioni aiutano a collegare tempo, immagine e comportamento.

## 5. Diagnosi guidata

### Sintomo: `/ready` fallisce

Controllare:

1. `BACKEND_URL` del frontend;
2. ingress backend interno;
3. stesso Container Apps Environment;
4. log frontend;
5. log backend;
6. AppDependencies.

### Sintomo: `/products/slow` è lento

Controllare:

1. latenza Prometheus/Grafana;
2. trace Jaeger locale;
3. `DurationMs` in AppRequests;
4. `DurationMs` in AppDependencies;
5. log backend.

### Sintomo: `/products/error` restituisce 500

Controllare:

1. AppRequests con ResultCode 500;
2. AppExceptions;
3. ContainerAppConsoleLogs;
4. trace Jaeger se in locale;
5. request_id nei log.

### Sintomo: log ACA presenti ma niente AppInsights

Controllare:

1. connection string Application Insights;
2. variabili ambiente;
3. librerie OpenTelemetry;
4. riavvio/revisione ACA dopo aggiornamento;
5. intervallo temporale della query.

## 6. Raccolta evidenze

Salvare in `evidence/`:

- output curl;
- query usate;
- screenshot o descrizione dashboard;
- trace id o request id significativo;
- incident report.

## 7. Regola pratica

Non chiudere un incident report con una causa se non hai almeno:

```text
1 segnale di sintomo
1 segnale di componente
1 segnale temporale
1 segnale che esclude un'ipotesi alternativa
```

# OBS UD17 - Guida operativa
# Application Insights, Log Analytics e KQL per Catalogo prodotti su ACA

## 1. Variabili operative

Adattare i valori al proprio ambiente.

```bash
RG="rg-obs-corso"
LOCATION="westeurope"
LAW_NAME="law-obs-corso"
APPINSIGHTS_NAME="appi-obs-products"
ACR_NAME="acrobscorso"
FRONTEND_APP_NAME="ca-obs-products-frontend"
BACKEND_APP_NAME="ca-obs-products-backend"
```

## 2. Verifica risorse Azure

```bash
az group show --name "$RG" -o table
az acr show --name "$ACR_NAME" --resource-group "$RG" -o table
```

Container Apps:

```bash
az containerapp show \
  --resource-group "$RG" \
  --name "$FRONTEND_APP_NAME" \
  --query "{name:name,fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName,external:properties.configuration.ingress.external}" \
  -o json

az containerapp show \
  --resource-group "$RG" \
  --name "$BACKEND_APP_NAME" \
  --query "{name:name,fqdn:properties.configuration.ingress.fqdn,latestRevision:properties.latestRevisionName,external:properties.configuration.ingress.external}" \
  -o json
```

## 3. Verifica variabili d'ambiente Container Apps

Per vedere le variabili effettive nella revisione:

```bash
az containerapp show \
  --resource-group "$RG" \
  --name "$FRONTEND_APP_NAME" \
  --query "properties.template.containers[0].env" \
  -o table

az containerapp show \
  --resource-group "$RG" \
  --name "$BACKEND_APP_NAME" \
  --query "properties.template.containers[0].env" \
  -o table
```

Controllare in particolare:

| Variabile | Frontend | Backend |
|---|---|---|
| `SERVICE_NAME` | `products-frontend` | `products-backend` |
| `APP_VERSION` | BuildId/tag | BuildId/tag |
| `APP_ENV` | `aca-observable` | `aca-observable` |
| `PORT` | `8000` | `8000` |
| `BACKEND_URL` | presente | non necessario |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | presente come secret/valore | presente come secret/valore |

## 4. Application Insights

Creazione CLI, se non già esistente:

```bash
LAW_ID=$(az monitor log-analytics workspace show \
  --resource-group "$RG" \
  --workspace-name "$LAW_NAME" \
  --query id \
  -o tsv)

az monitor app-insights component create \
  --app "$APPINSIGHTS_NAME" \
  --location "$LOCATION" \
  --resource-group "$RG" \
  --application-type web \
  --workspace "$LAW_ID"
```

Connection string:

```bash
APPINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show \
  --app "$APPINSIGHTS_NAME" \
  --resource-group "$RG" \
  --query connectionString \
  -o tsv)

echo "$APPINSIGHTS_CONNECTION_STRING"
```

Non committare questo valore. Inserirlo in Azure DevOps come variabile segreta.

## 5. Verifica endpoint applicativi

```bash
FRONTEND_URL="https://$(az containerapp show \
  --resource-group "$RG" \
  --name "$FRONTEND_APP_NAME" \
  --query properties.configuration.ingress.fqdn \
  -o tsv)"

echo "$FRONTEND_URL"

curl -i "$FRONTEND_URL/health"
curl -i "$FRONTEND_URL/ready"
curl -i "$FRONTEND_URL/version"
curl -i "$FRONTEND_URL/products"
curl -i "$FRONTEND_URL/products/slow"
curl -i "$FRONTEND_URL/products/error"
```

`/products/error` deve restituire 500 controllato. Non è un fallimento del laboratorio: è un segnale da osservare.

## 6. Generazione traffico automatica

```bash
bash work/UD17/scripts/generate_traffic_products.sh "$FRONTEND_URL"
```

Lo script produce:

- molte chiamate normali a `/products`;
- chiamate lente a `/products/slow`;
- errori controllati a `/products/error` ogni alcuni cicli;
- `X-Request-Id` leggibili.

Attendere alcuni minuti prima di interrogare KQL.

## 7. Query KQL principali

### 7.1 Ultime request

```kql
AppRequests
| where TimeGenerated > ago(2h)
| project TimeGenerated, AppRoleName, Name, Url, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

### 7.2 Solo traffico products

```kql
AppRequests
| where TimeGenerated > ago(2h)
| where Url has "/products" or Name has "/products"
| summarize Requests=count(), AvgDurationMs=avg(DurationMs), P95DurationMs=percentile(DurationMs, 95) by AppRoleName, Name, ResultCode, Success
| order by Requests desc
```

### 7.3 Dependency frontend → backend

```kql
AppDependencies
| where TimeGenerated > ago(2h)
| where Name has "/api/products" or Data has "/api/products" or Target has "backend"
| project TimeGenerated, AppRoleName, Target, Name, Data, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

### 7.4 Endpoint lento

```kql
AppRequests
| where TimeGenerated > ago(2h)
| where Url has "/products/slow" or Name has "/products/slow"
| project TimeGenerated, AppRoleName, Name, ResultCode, Success, DurationMs, OperationId
| order by DurationMs desc
```

### 7.5 Errori controllati

```kql
AppRequests
| where TimeGenerated > ago(2h)
| where Url has "/products/error" or Name has "/products/error" or toint(ResultCode) >= 500
| project TimeGenerated, AppRoleName, Name, Url, ResultCode, Success, DurationMs, OperationId
| order by TimeGenerated desc
```

### 7.6 Log container JSON

```kql
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(2h)
| where Log_s has "request_id"
| extend j=parse_json(Log_s)
| project TimeGenerated, ContainerAppName_s, RevisionName_s, service=tostring(j.service), path=tostring(j.path), status=toint(j.status), latency_ms=todouble(j.latency_ms), request_id=tostring(j.request_id), trace_id=tostring(j.trace_id), message=tostring(j.message)
| order by TimeGenerated desc
```

### 7.7 Ricerca per request_id

```kql
let rid = "INCOLLA_REQUEST_ID";
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(2h)
| where Log_s has rid
| extend j=parse_json(Log_s)
| project TimeGenerated, ContainerAppName_s, service=tostring(j.service), path=tostring(j.path), status=toint(j.status), latency_ms=todouble(j.latency_ms), request_id=tostring(j.request_id), trace_id=tostring(j.trace_id)
| order by TimeGenerated asc
```

## 8. Troubleshooting operativo

| Sintomo | Causa probabile | Verifica |
|---|---|---|
| `/health` OK ma `/ready` KO | frontend non raggiunge backend | `BACKEND_URL`, ingress backend, log frontend |
| AppRequests vuota | telemetry non inviata o ritardo | connection string, variabile pipeline, attendere |
| Log ACA presenti ma niente dependencies | traffico solo su `/health` o strumentazione client non attiva | generare `/products`, controllare codice frontend |
| `/products/error` non restituisce 500 | vecchia immagine o rotta diversa | `/version`, revisione attiva, tag immagine |
| Home non mostra catalogo | frontend non aggiornato o backend non raggiunto | `/products`, `/ready`, log frontend |
| Query KQL senza risultati | workspace errato o finestra troppo stretta | usare `ago(24h)`, controllare LAW/App Insights |

## 9. Criterio di successo

La UD17 è riuscita quando il partecipante può mostrare:

- frontend e backend ACA aggiornati alla versione osservabile;
- `/products`, `/products/slow`, `/products/error` testati;
- almeno una request frontend in Application Insights;
- almeno una dependency frontend → backend;
- almeno un log JSON frontend e backend in `ContainerAppConsoleLogs_CL`;
- almeno una analisi di latenza o errore;
- un decision record basato su evidenze.

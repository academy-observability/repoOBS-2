# Evidence UD17 - Observability cloud Catalogo prodotti

## 1. Dati ambiente

| Campo | Valore |
|---|---|
| Resource Group |  |
| Azure Container Registry |  |
| ACA Environment |  |
| Frontend Container App |  |
| Backend Container App |  |
| Application Insights |  |
| Log Analytics Workspace |  |
| Pipeline run / Build ID |  |
| Immagine backend | `obsapp-products-backend:` |
| Immagine frontend | `obsapp-products-frontend:` |

## 2. Endpoint testati

| Endpoint | Status | Note |
|---|---:|---|
| `/health` |  |  |
| `/ready` |  |  |
| `/version` |  |  |
| `/products` |  |  |
| `/products/slow` |  |  |
| `/products/error` |  |  |
| `/` home Catalogo prodotti |  |  |

## 3. Request ID usati

| Caso | Request ID | Endpoint |
|---|---|---|
| Normale |  | `/products` |
| Lento |  | `/products/slow` |
| Errore |  | `/products/error` |

## 4. Query KQL eseguite

| Query | Tabella | Risultato osservato |
|---|---|---|
| Ultime request products | AppRequests |  |
| Dependency FE → BE | AppDependencies |  |
| Log JSON products | ContainerAppConsoleLogs_CL |  |
| Endpoint lento | AppRequests / logs |  |
| Errore controllato | AppRequests / logs |  |
| Ricerca per request_id | ContainerAppConsoleLogs_CL |  |

## 5. Correlazione FE → BE

| Elemento | Evidenza |
|---|---|
| Request frontend |  |
| Dependency frontend → backend |  |
| Request backend |  |
| Log frontend |  |
| Log backend |  |
| OperationId / request_id / trace_id |  |

## 6. Decision record

```text
Osservazione:
Evidenza principale:
Evidenza secondaria:
Ipotesi:
Verifica:
Decisione tecnica:
Limite dell'analisi:
```

## 7. Note finali

Indicare eventuali problemi:

- ritardo ingestion Application Insights;
- workspace sbagliato;
- variabili non impostate;
- nuova revisione non attiva;
- endpoint non raggiungibile;
- log non ancora disponibili.

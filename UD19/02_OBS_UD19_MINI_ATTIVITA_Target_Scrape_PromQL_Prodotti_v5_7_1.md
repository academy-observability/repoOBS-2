# OBS UD19 — Mini-attività
# Target, scrape e PromQL sul Catalogo prodotti

Compila la tabella dopo aver avviato lo stack e aperto Prometheus.

## 1. Target Prometheus

| Target/job | Endpoint scrape | Stato | Cosa significa se è DOWN |
|---|---|---|---|
| `products-backend` | `backend-products:8000/metrics` | | |
| `products-frontend` | `frontend-products:8080/metrics` | | |
| `prometheus` | `localhost:9090/metrics` | | |

## 2. Metriche principali

| Metrica | Tipo logico | Cosa misura | Perché è utile |
|---|---|---|---|
| `up` | gauge | | |
| `app_http_requests_total` | counter | | |
| `app_http_request_duration_seconds` | histogram | | |

## 3. Query e interpretazione

Completa la colonna “Risposta tecnica”.

| Domanda | Query PromQL | Risposta tecnica |
|---|---|---|
| Prometheus vede i target? | `up` | |
| Quante richieste per servizio/path/status? | `sum by (service,path,status) (app_http_requests_total)` | |
| Qual è il rate richieste recente? | `sum by (service,path,status) (rate(app_http_requests_total[2m]))` | |
| Ci sono errori 5xx? | `sum by (service,path,status) (rate(app_http_requests_total{status=~"5.."}[2m]))` | |
| Qual è la latenza media recente? | `sum by (service,path) (rate(app_http_request_duration_seconds_sum[2m])) / sum by (service,path) (rate(app_http_request_duration_seconds_count[2m]))` | |

## 4. Domande brevi

1. Perché Prometheus usa `backend-products:8000` e non `localhost:8018`?
2. Che differenza c'è tra counter assoluto e `rate()`?
3. Perché `/products/slow` è utile per il laboratorio?
4. Perché `/products/error` non è “un problema da correggere” durante il test?
5. Che cosa osserviamo in UD19 che useremo poi in Grafana e negli alert?

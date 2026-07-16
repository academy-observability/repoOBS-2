# Query PromQL UD19 — Catalogo prodotti

## Disponibilità target

```promql
up
```

```promql
up{job="products-backend"}
```

```promql
up{job="products-frontend"}
```

## Richieste totali per servizio, path e status

```promql
sum by (service, path, status) (app_http_requests_total)
```

## Rate richieste ultimi 2 minuti

```promql
sum by (service, path, status) (
  rate(app_http_requests_total[2m])
)
```

## Error rate 5xx

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{status=~"5.."}[2m])
)
```

## Latenza media

```promql
sum by (service, path) (rate(app_http_request_duration_seconds_sum[2m]))
/
sum by (service, path) (rate(app_http_request_duration_seconds_count[2m]))
```

## p95 latenza

```promql
histogram_quantile(
  0.95,
  sum by (le, service, path) (
    rate(app_http_request_duration_seconds_bucket[2m])
  )
)
```

## Filtri utili

```promql
sum by (path, status) (app_http_requests_total{service="product-frontend"})
```

```promql
sum by (path, status) (app_http_requests_total{service="product-backend"})
```

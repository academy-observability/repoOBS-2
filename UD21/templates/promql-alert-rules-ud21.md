# UD21 — PromQL di riferimento per alert candidati

## 1. Target frontend o backend non raggiunto da Prometheus

```promql
up{job=~"products-.*"} == 0
```

Uso: rileva la perdita di capacità di scrape. Non dimostra da solo che l'applicazione sia indisponibile, ma segnala che Prometheus non la sta osservando.

---

## 2. Error rate user-facing robusto

```promql
(
  sum(
    rate(
      app_http_requests_total{
        service="products-frontend",
        path=~"/products.*",
        status=~"5.."
      }[2m]
    )
  ) or vector(0)
)
/
clamp_min(
  sum(
    rate(
      app_http_requests_total{
        service="products-frontend",
        path=~"/products.*"
      }[2m]
    )
  ) or vector(0),
  0.001
)
```

Soglia didattica:

```text
A IS ABOVE 0.20
Pending period: 1m
```

Perché è robusta:

- `or vector(0)` evita serie assente per i 5xx;
- `clamp_min` evita divisione per zero;
- il filtro frontend evita doppio conteggio della richiesta distribuita.

---

## 3. Errori per servizio, path e status

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{status=~"5.."}[1m])
)
```

Uso: query diagnostica, non necessariamente alert principale.

---

## 4. Latenza p95 user-facing

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(
      app_http_request_duration_seconds_bucket{
        service="products-frontend",
        path=~"/products.*"
      }[2m]
    )
  )
)
```

Soglia didattica:

```text
A IS ABOVE 1.5
Pending period: 1m
```

---

## 5. Readiness non riuscita

```promql
sum(
  rate(
    app_http_requests_total{
      service="products-frontend",
      path="/ready",
      status!~"2.."
    }[2m]
  )
) > 0
```

Uso: rileva fallimenti del controllo frontend → backend.

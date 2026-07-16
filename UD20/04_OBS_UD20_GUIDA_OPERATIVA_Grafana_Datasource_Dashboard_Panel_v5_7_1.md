# OBS UD20 — Guida operativa
# Grafana datasource, dashboard, pannelli e troubleshooting

## 0. Scopo

Questa guida serve quando Grafana non mostra quello che ci aspettiamo o quando vogliamo capire meglio il rapporto tra datasource, dashboard, pannelli e query PromQL.

---

## 1. Verifica rapida dei servizi

```bash
docker compose ps
```

Servizi attesi:

```text
ud20-products-backend
ud20-products-frontend
ud20-prometheus
ud20-grafana
ud20-jaeger
```

URL:

```text
Frontend    http://localhost:8120/
Backend     http://localhost:8020/health
Prometheus  http://localhost:9090
Grafana     http://localhost:3000
Jaeger      http://localhost:16686
```

---

## 2. Datasource Prometheus

Il datasource è provisionato in:

```text
grafana/provisioning/datasources/prometheus.yml
```

Valore importante:

```yaml
url: http://prometheus:9090
```

Dentro il container Grafana, `prometheus` è il nome del servizio Docker. Dal browser invece Prometheus si apre con `http://localhost:9090`.

---

## 3. Dashboard provisionata

La dashboard è in:

```text
grafana/dashboards/ud20-products-dashboard.json
```

Il provider è in:

```text
grafana/provisioning/dashboards/dashboards.yml
```

Se la dashboard non compare:

```bash
docker logs ud20-grafana --tail 100
```

Controllare errori di parsing JSON o path errati.

---

## 4. Problemi frequenti

### 4.1 Grafana si apre ma non vedo dati

Controllare:

```text
1. Time range in alto a destra: usare Last 15 minutes.
2. Prometheus target UP.
3. Traffico generato dopo l'avvio dello stack.
4. Query PromQL funzionante in Prometheus.
```

### 4.2 Datasource non funziona

Da Grafana:

```text
Connections → Data sources → Prometheus → Save & test
```

Se fallisce, controllare:

```bash
docker logs ud20-grafana --tail 80
docker compose ps
```

### 4.3 Pannello errori vuoto

Può essere normale se non è stato chiamato:

```text
/products/error
```

Generare traffico:

```bash
./scripts/generate_traffic_ud20.sh
```

Oppure manualmente:

```bash
curl -i http://localhost:8120/products/error
```

### 4.4 Latenza non evidente

Controllare che sia stato chiamato:

```text
/products/slow
```

E usare una finestra di almeno 5 minuti nella query p95.

### 4.5 Query corretta ma pannello poco leggibile

Intervenire su:

```text
Legend
Unità di misura
Titolo pannello
Time range
Tipo pannello: Time series / Table / Stat
```

---

## 5. Query utili

Target:

```promql
up{job=~"products-.*"}
```

Request rate:

```promql
sum by (service,path,status) (rate(app_http_requests_total{path=~"/|/products.*|/ready"}[1m]))
```

Error rate:

```promql
sum by (service,path,status) (rate(app_http_requests_total{status=~"5.."}[1m]))
```

Latenza media:

```promql
sum by (service,path) (rate(app_http_request_duration_seconds_sum{path=~"/|/products.*"}[5m]))
/
sum by (service,path) (rate(app_http_request_duration_seconds_count{path=~"/|/products.*"}[5m]))
```

P95:

```promql
histogram_quantile(
  0.95,
  sum by (le, service, path) (
    rate(app_http_request_duration_seconds_bucket{path=~"/|/products.*"}[5m])
  )
)
```

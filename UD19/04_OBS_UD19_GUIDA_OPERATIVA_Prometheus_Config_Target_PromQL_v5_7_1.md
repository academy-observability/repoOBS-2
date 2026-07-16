# OBS UD19 — Guida operativa
# Prometheus, prometheus.yml, target e query PromQL

## 0. Scopo

Questa guida aiuta a leggere e diagnosticare la parte Prometheus dello stack locale. È pensata per essere consultata durante il laboratorio quando un target non sale, una query non restituisce dati o le metriche non sembrano cambiare dopo il traffico.

---

## 1. File principale: prometheus.yml

Percorso:

```text
src/app_products_prometheus/prometheus/prometheus.yml
```

Contenuto logico:

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: "products-backend"
    metrics_path: /metrics
    static_configs:
      - targets: ["backend-products:8000"]

  - job_name: "products-frontend"
    metrics_path: /metrics
    static_configs:
      - targets: ["frontend-products:8080"]
```

`static_configs` significa che dichiariamo manualmente i target. In ambienti più dinamici si possono usare meccanismi di service discovery, ma qui vogliamo vedere chiaramente chi osserva chi.

---

## 2. Comandi Docker utili

Verificare container:

```bash
docker compose ps
```

Verificare log Prometheus:

```bash
docker compose logs prometheus --tail=100
```

Verificare che Prometheus sia nella rete corretta:

```bash
docker inspect prometheus --format '{{json .NetworkSettings.Networks}}' | jq
```

Senza `jq`:

```bash
docker inspect prometheus | grep -A5 Networks
```

---

## 3. Verificare /metrics manualmente

Dal PC host:

```bash
curl -s http://localhost:8018/metrics | grep app_http | head
curl -s http://localhost:8118/metrics | grep app_http | head
```

Da dentro il container Prometheus, se serve:

```bash
docker exec prometheus wget -qO- http://backend-products:8000/metrics | head
```

Questa verifica distingue due problemi diversi:

| Caso | Interpretazione |
|---|---|
| `/metrics` non risponde dal PC | problema app/porta/container |
| `/metrics` risponde dal PC ma non da Prometheus | problema rete Docker/nome target |
| `/metrics` risponde ma query vuota | problema nome metrica/finestra temporale/assenza traffico |

---

## 4. Query base

### Target disponibili

```promql
up
```

### Richieste totali

```promql
sum by (service, path, status) (app_http_requests_total)
```

### Request rate

```promql
sum by (service, path, status) (
  rate(app_http_requests_total[2m])
)
```

### Error rate

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{status=~"5.."}[2m])
)
```

### Latenza media

```promql
sum by (service, path) (rate(app_http_request_duration_seconds_sum[2m]))
/
sum by (service, path) (rate(app_http_request_duration_seconds_count[2m]))
```

### p95

```promql
histogram_quantile(
  0.95,
  sum by (le, service, path) (
    rate(app_http_request_duration_seconds_bucket[2m])
  )
)
```

---

## 5. Troubleshooting frequente

### Target DOWN

Controllare:

```bash
docker compose ps
cat prometheus/prometheus.yml
docker compose logs prometheus --tail=100
```

Cause frequenti:

- nome servizio errato;
- porta container errata;
- app non partita;
- container non nella stessa rete;
- endpoint `/metrics` non disponibile.

### Query senza dati

Possibili cause:

- non è stato generato traffico;
- finestra `[2m]` troppo stretta rispetto agli scrape;
- nome metrica scritto male;
- Prometheus appena avviato e non ha ancora raccolto abbastanza campioni.

Azioni:

```bash
./scripts/generate_traffic_ud19.sh
```

attendere 20-30 secondi e riprovare.

### Error rate sempre vuoto

Generare errori controllati:

```bash
for i in {1..10}; do curl -s -o /dev/null http://localhost:8118/products/error || true; done
```

Poi rieseguire la query sugli status 5xx.

### Latenza non cambia

Generare traffico lento:

```bash
for i in {1..10}; do curl -s -o /dev/null http://localhost:8118/products/slow || true; done
```

La latenza può richiedere qualche scrape per essere visibile.

---

## 6. Frase diagnostica utile

Quando una query non restituisce il dato atteso, non diciamo genericamente “Prometheus non funziona”. Seguiamo questa catena:

```text
container UP?
endpoint /metrics raggiungibile?
target Prometheus UP?
metrica presente?
traffico generato?
finestra temporale adeguata?
query PromQL corretta?
```

Questa catena evita diagnosi frettolose.

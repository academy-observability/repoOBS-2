# OBS UD19 — Laboratorio guidato
# Prometheus osserva il Catalogo prodotti FE/BE

## 0. Obiettivo del laboratorio

In questo laboratorio usiamo Prometheus per osservare localmente l'applicazione **Catalogo prodotti** composta da frontend e backend. Lo stack nasce dalla UD18, ma qui cambiamo il punto di attenzione: non ci interessa soltanto che i container siano avviati; ci interessa che Prometheus riesca a raccogliere metriche e che noi sappiamo interrogarle.

Alla fine dovremo dimostrare:

```text
Prometheus vede frontend e backend come target UP.
Frontend e backend espongono /metrics.
Il traffico su /products aumenta i counter.
/products/slow modifica la latenza.
/products/error produce errori osservabili.
PromQL consente di leggere traffico, errori e durata.
```

---

## 1. Preparazione della cartella di lavoro

Copiamo il materiale UD19 nel repository del corso.

Struttura attesa:

```text
work/UD19/
├── src/app_products_prometheus/
│   ├── docker-compose.yml
│   ├── backend/
│   ├── frontend/
│   ├── prometheus/prometheus.yml
│   ├── grafana/provisioning/datasources/prometheus.yml
│   └── scripts/
├── docs/
├── evidence/
└── logs/
```

Entriamo nella cartella dello stack:

```bash
cd work/UD19/src/app_products_prometheus
```

Verifichiamo i file principali:

```bash
find . -maxdepth 3 -type f | sort
```

Devono comparire almeno:

```text
./backend/app.py
./frontend/app.py
./docker-compose.yml
./prometheus/prometheus.yml
./scripts/start_stack_ud19.sh
./scripts/generate_traffic_ud19.sh
./scripts/stop_stack_ud19.sh
```

---

## 2. Lettura della configurazione Prometheus

Apriamo:

```text
prometheus/prometheus.yml
```

Osserviamo tre blocchi:

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s
```

Qui definiamo ogni quanto Prometheus raccoglie le metriche.

Poi:

```yaml
- job_name: "products-backend"
  metrics_path: /metrics
  static_configs:
    - targets: ["backend-products:8000"]
```

Infine:

```yaml
- job_name: "products-frontend"
  metrics_path: /metrics
  static_configs:
    - targets: ["frontend-products:8080"]
```

Il punto chiave è questo: Prometheus non usa `localhost:8018` o `localhost:8118` per parlare con i container. Usa i nomi Docker interni `backend-products` e `frontend-products` perché si trova nella stessa rete dello stack.

---

## 3. Avvio dello stack

Eseguiamo:

```bash
./scripts/start_stack_ud19.sh
```

In alternativa:

```bash
docker compose up -d --build
```

Verifichiamo i container:

```bash
docker compose ps
```

Output atteso, in forma simile:

```text
backend-products      running
frontend-products     running
prometheus            running
grafana               running
jaeger                running
```

---

## 4. Verifica endpoint applicativi

Dal PC/WSL verifichiamo il frontend:

```bash
curl -i http://localhost:8118/health
curl -i http://localhost:8118/ready
curl -i http://localhost:8118/products
```

Verifichiamo anche il backend:

```bash
curl -i http://localhost:8018/health
curl -i http://localhost:8018/api/products
```

Risultati attesi:

| Endpoint | Esito atteso |
|---|---|
| frontend `/health` | HTTP 200 |
| frontend `/ready` | HTTP 200, backend raggiungibile |
| frontend `/products` | HTTP 200, catalogo prodotti |
| backend `/health` | HTTP 200 |
| backend `/api/products` | HTTP 200, JSON prodotti |

---

## 5. Verifica endpoint /metrics

Ora controlliamo che le app espongano metriche Prometheus.

Frontend:

```bash
curl -s http://localhost:8118/metrics | head -40
```

Backend:

```bash
curl -s http://localhost:8018/metrics | head -40
```

Cerchiamo metriche come:

```text
app_http_requests_total
app_http_request_duration_seconds_bucket
app_http_request_duration_seconds_count
app_http_request_duration_seconds_sum
```

Questa verifica è importante: se `/metrics` non funziona, Prometheus non può raccogliere metriche applicative.

---

## 6. Apertura Prometheus

Apriamo nel browser:

```text
http://localhost:9090
```

Andiamo in:

```text
Status → Targets
```

Devono essere presenti e `UP`:

```text
products-backend
products-frontend
prometheus
```

Se un target è `DOWN`, non passiamo subito alle query. Prima analizziamo:

```bash
docker compose ps
cat prometheus/prometheus.yml
docker compose logs prometheus --tail=100
```

---

## 7. Prima query: up

Nella pagina Graph di Prometheus eseguiamo:

```promql
up
```

Interpretazione:

| Valore | Significato |
|---:|---|
| `1` | target raggiungibile |
| `0` | target non raggiungibile |

Poi proviamo:

```promql
up{job="products-backend"}
```

E:

```promql
up{job="products-frontend"}
```

Questa query non dice se l'applicazione è funzionalmente corretta. Dice se Prometheus riesce a raccogliere metriche dal target.

---

## 8. Generazione traffico

Eseguiamo lo script:

```bash
./scripts/generate_traffic_ud19.sh
```

Lo script chiama più volte:

```text
/products
/products/slow
/products/error
/ready
```

Possiamo aumentare il traffico:

```bash
ROUNDS=80 ./scripts/generate_traffic_ud19.sh
```

Attendiamo almeno 20-30 secondi per dare a Prometheus il tempo di effettuare alcuni scrape.

---

## 9. Query richieste totali

In Prometheus eseguiamo:

```promql
sum by (service, path, status) (app_http_requests_total)
```

Dobbiamo riconoscere righe relative a:

```text
frontend /products 200
frontend /products/slow 200
frontend /products/error 500 oppure 503
backend /api/products 200
backend /api/products/slow 200
backend /api/products/error 500
```

L'obiettivo non è memorizzare il numero esatto, ma capire che il traffico generato lascia traccia nei counter.

---

## 10. Query request rate

Eseguiamo:

```promql
sum by (service, path, status) (
  rate(app_http_requests_total[2m])
)
```

Questa query ci dice il ritmo recente delle richieste. È più utile del counter assoluto quando vogliamo capire se in questo momento l'applicazione sta ricevendo traffico.

Se non vediamo valori, generiamo altro traffico e riproviamo.

---

## 11. Query error rate

Eseguiamo:

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{status=~"5.."}[2m])
)
```

Poi generiamo errori:

```bash
for i in {1..10}; do curl -s -o /dev/null http://localhost:8118/products/error || true; done
```

Riproviamo la query.

Dobbiamo vedere aumentare la serie relativa agli endpoint di errore. Questo è il punto di passaggio verso UD21: un errore ripetuto diventa una possibile condizione di alert.

---

## 12. Query latenza media

Eseguiamo:

```promql
sum by (service, path) (rate(app_http_request_duration_seconds_sum[2m]))
/
sum by (service, path) (rate(app_http_request_duration_seconds_count[2m]))
```

Poi generiamo traffico lento:

```bash
for i in {1..10}; do curl -s -o /dev/null http://localhost:8118/products/slow || true; done
```

Riproviamo la query.

Dobbiamo confrontare `/products` e `/products/slow`.

---

## 13. Query p95

Eseguiamo:

```promql
histogram_quantile(
  0.95,
  sum by (le, service, path) (
    rate(app_http_request_duration_seconds_bucket[2m])
  )
)
```

Questa query è più avanzata. Non è necessario che tutti la padroneggino subito, ma devono capire il senso: p95 indica una latenza sotto la quale cade circa il 95% delle richieste osservate nel periodo.

---

## 14. Evidenze da salvare

Creiamo o compiliamo:

```text
docs/evidence_ud19.md
```

Inseriamo:

```markdown
# Evidence UD19

## Target Prometheus
- products-backend: UP/DOWN
- products-frontend: UP/DOWN

## Query eseguite
- up
- app_http_requests_total
- rate richieste
- error rate
- latenza media
- p95

## Osservazioni
- cosa cambia dopo /products
- cosa cambia dopo /products/slow
- cosa cambia dopo /products/error

## Screenshot consigliati
- pagina Targets
- query traffico
- query errori
- query latenza
```

---

## 15. Chiusura

Fermiamo lo stack:

```bash
./scripts/stop_stack_ud19.sh
```

Oppure:

```bash
docker compose down
```

Frase conclusiva attesa:

> Ho verificato che Prometheus raccoglie metriche da frontend e backend. Ho generato traffico normale, lento ed errato sul Catalogo prodotti e ho interrogato le metriche con PromQL per distinguere disponibilità, volume, errori e latenza.

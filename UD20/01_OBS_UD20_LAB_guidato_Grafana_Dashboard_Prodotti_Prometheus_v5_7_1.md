# OBS UD20 — Laboratorio guidato
# Grafana dashboard per il Catalogo prodotti osservato da Prometheus

## 0. Obiettivo del laboratorio

In questo laboratorio usiamo lo stack locale già introdotto nelle UD18–UD19 e costruiamo una dashboard Grafana per osservare il comportamento dell'app **Catalogo prodotti**.

Il risultato finale deve essere una dashboard capace di mostrare:

- disponibilità dei target Prometheus;
- traffico HTTP su frontend e backend;
- errori 5xx;
- latenza media e p95;
- differenza tra endpoint normale, lento ed errore.

---

## 1. Preparazione ambiente

Apriamo la cartella della UD20:

```bash
cd UD20/src/app_products_grafana
```

Avviamo lo stack:

```bash
./scripts/start_stack_ud20.sh
```

Controlliamo i container:

```bash
docker compose ps
```

Output atteso: devono essere in esecuzione almeno:

```text
ud20-products-backend
ud20-products-frontend
ud20-prometheus
ud20-grafana
ud20-jaeger
```

---

## 2. Verifica applicazione

Verifichiamo il frontend:

```bash
curl -i http://localhost:8120/health
curl -i http://localhost:8120/ready
curl -i http://localhost:8120/products
```

Verifichiamo il backend:

```bash
curl -i http://localhost:8020/health
curl -i http://localhost:8020/api/products
```

La home deve essere visibile nel browser:

```text
http://localhost:8120/
```

---

## 3. Verifica Prometheus prima di Grafana

Apriamo Prometheus:

```text
http://localhost:9090
```

Andiamo in:

```text
Status → Targets
```

Devono essere `UP`:

```text
products-backend
products-frontend
```

Proviamo una query semplice:

```promql
up{job=~"products-.*"}
```

Poi:

```promql
sum by (service, path, status) (app_http_requests_total)
```

Se Prometheus non ha dati, Grafana non potrà mostrarli correttamente.

---

## 4. Accesso a Grafana

Apriamo:

```text
http://localhost:3000
```

Credenziali:

```text
admin / admin
```

Se Grafana chiede di cambiare password, possiamo saltare o confermare una password temporanea secondo le impostazioni locali del laboratorio.

---

## 5. Verifica datasource Prometheus

Dal menu Grafana:

```text
Connections → Data sources → Prometheus
```

Verifichiamo:

```text
URL: http://prometheus:9090
```

Usiamo:

```text
Save & test
```

Risultato atteso:

```text
Successfully queried the Prometheus API
```

Nota tecnica: l'URL è `http://prometheus:9090` perché Grafana interroga Prometheus dalla rete Docker interna, non dal nostro browser.

---

## 6. Apertura dashboard provisionata

La dashboard dovrebbe essere già caricata dal provisioning.

Percorso:

```text
Dashboards → Academy Observability → UD20 - Catalogo prodotti - FE/BE metrics
```

Se non compare subito, attendiamo qualche secondo e aggiorniamo la pagina. In alternativa controlliamo i log di Grafana:

```bash
docker logs ud20-grafana --tail 80
```

---

## 7. Generazione traffico

Eseguiamo lo script:

```bash
./scripts/generate_traffic_ud20.sh
```

Lo script genera traffico su:

```text
/
/products
/ready
/products/slow
/products/error
```

Durante o dopo l'esecuzione osserviamo la dashboard Grafana.

---

## 8. Lettura dei pannelli

### 8.1 Target UP

Questo pannello deve mostrare che frontend e backend sono raggiungibili da Prometheus.

Domanda da porsi:

```text
Se un servizio è DOWN, ha senso fidarsi degli altri pannelli?
```

Risposta: bisogna prima capire perché Prometheus non riesce a raccogliere da quel target.

### 8.2 Request rate

Il pannello deve crescere mentre lo script genera traffico.

PromQL usata:

```promql
sum by (service,path,status) (rate(app_http_requests_total{path=~"/|/products.*|/ready"}[1m]))
```

### 8.3 Error rate 5xx

Il pannello deve mostrare traffico quando viene chiamato:

```text
/products/error
```

PromQL:

```promql
sum by (service,path,status) (rate(app_http_requests_total{status=~"5.."}[1m]))
```

### 8.4 Latency p95

Il pannello deve evidenziare il comportamento di:

```text
/products/slow
```

PromQL:

```promql
histogram_quantile(
  0.95,
  sum by (le, service, path) (
    rate(app_http_request_duration_seconds_bucket{path=~"/|/products.*"}[5m])
  )
)
```

---

## 9. Creazione manuale di un pannello aggiuntivo

Anche se la dashboard è provisionata, creiamo un pannello manuale per capire il processo.

```text
Dashboard → Edit → Add visualization
```

Datasource:

```text
Prometheus
```

Query:

```promql
sum by (service, path) (rate(app_http_requests_total[1m]))
```

Titolo pannello:

```text
UD20 - Request rate manuale
```

Salviamo la dashboard con nome:

```text
UD20 - Catalogo prodotti - esercizio partecipante
```

---

## 10. Evidenze da salvare

Creiamo o aggiorniamo:

```text
docs/evidence_ud20.md
```

Inseriamo:

```markdown
# Evidenze UD20

## Stack
- Frontend URL:
- Backend URL:
- Prometheus URL:
- Grafana URL:

## Datasource
- Nome datasource:
- URL datasource:
- Esito Save & test:

## Dashboard
- Nome dashboard:
- Pannelli verificati:

## Query principali
- Request rate:
- Error rate:
- Latency p95:

## Osservazioni
- Che cosa cambia dopo /products/slow:
- Che cosa cambia dopo /products/error:
- Differenza osservata tra frontend e backend:
```

---

## 11. Cleanup

A fine attività:

```bash
./scripts/stop_stack_ud20.sh
```

---

## 12. Frase finale attesa

Il partecipante deve saper dire:

> Ho usato Grafana per trasformare le metriche Prometheus dell'app Catalogo prodotti in una dashboard operativa. Ho verificato datasource, target, traffico, errori e latenza, e ho collegato ogni pannello a una domanda tecnica precisa.

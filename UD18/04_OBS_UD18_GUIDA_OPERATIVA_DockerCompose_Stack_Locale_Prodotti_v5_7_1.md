# OBS UD18 — Guida operativa
# Docker Compose, controlli, troubleshooting e ripartenza stack locale

## 0. Scopo

Questa guida raccoglie i comandi operativi essenziali per gestire lo stack locale UD18. È pensata per essere usata durante il laboratorio e per il troubleshooting.

---

## 1. Comandi base

Posizionarsi nella cartella:

```bash
cd work/UD18/app_products_local
```

Avvio con build:

```bash
docker compose up -d --build
```

Stato servizi:

```bash
docker compose ps
```

Log sintetici:

```bash
docker compose logs --tail=50
```

Stop:

```bash
docker compose down
```

Stop con volumi:

```bash
docker compose down -v
```

---

## 2. Controlli applicativi

Frontend:

```bash
curl -i http://localhost:8118/health
curl -i http://localhost:8118/ready
curl -i http://localhost:8118/products
```

Backend:

```bash
curl -i http://localhost:8018/health
curl -i http://localhost:8018/api/products
```

Metriche:

```bash
curl -s http://localhost:8118/metrics | head
curl -s http://localhost:8018/metrics | head
```

---

## 3. Controlli osservabilità

Prometheus:

```text
http://localhost:9090/targets
```

Grafana:

```text
http://localhost:3000
```

Jaeger:

```text
http://localhost:16686
```

---

## 4. Diagnosi problemi frequenti

### 4.1 Un container non parte

```bash
docker compose ps
docker compose logs NOME_SERVIZIO
```

Controllare:

- errore Python;
- dipendenze mancanti;
- porta già occupata;
- variabile d'ambiente errata.

### 4.2 Porta già occupata

Sintomo:

```text
Bind for 0.0.0.0:3000 failed
```

Soluzioni:

- chiudere il processo che usa la porta;
- cambiare porta host nel compose;
- evitare di avviare due stack simili contemporaneamente.

### 4.3 `/ready` fallisce

Controllare `BACKEND_URL` nel compose:

```yaml
BACKEND_URL: http://backend-products:8000
```

Poi verificare:

```bash
docker compose logs frontend-products
docker compose logs backend-products
```

### 4.4 Prometheus target DOWN

Controllare il file:

```text
prometheus/prometheus.yml
```

I target devono usare nomi container/servizio:

```text
backend-products:8000
frontend-products:8000
```

Non devono usare `localhost`.

### 4.5 Grafana datasource non funziona

Il datasource deve puntare a:

```text
http://prometheus:9090
```

Non a:

```text
http://localhost:9090
```

perché Grafana gira in container.

### 4.6 Jaeger non mostra trace

Generare traffico:

```bash
./scripts/generate_traffic_ud18.sh
```

Poi controllare:

```bash
docker compose logs jaeger
docker compose logs frontend-products
docker compose logs backend-products
```

Verificare la variabile:

```text
OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
```

---

## 5. Pulizia controllata

Pulizia standard:

```bash
docker compose down
```

Pulizia più forte:

```bash
docker compose down -v --remove-orphans
```

Pulizia immagini create nel laboratorio:

```bash
docker image ls | grep ud18
```

Rimuovere solo immagini chiaramente legate al laboratorio, se necessario.

---

## 6. Regola diagnostica

Quando un test fallisce, non cambiamo subito file a caso. Seguiamo la catena:

```text
container running?
  ↓
porta corretta?
  ↓
endpoint risponde?
  ↓
rete interna corretta?
  ↓
strumento osservante configurato?
  ↓
log/metriche/trace presenti?
```

Questa sequenza riduce diagnosi casuali e rende il troubleshooting più professionale.

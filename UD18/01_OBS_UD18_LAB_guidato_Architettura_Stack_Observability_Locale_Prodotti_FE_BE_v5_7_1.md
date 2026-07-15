# OBS UD18 — Laboratorio guidato
# Avvio dello stack locale Catalogo prodotti + Prometheus/Grafana/Jaeger

## 0. Obiettivo operativo

In questo laboratorio avviamo localmente uno stack completo composto da applicazione e strumenti osservanti.

Non stiamo ancora approfondendo PromQL, dashboard Grafana o tracing Jaeger: quelli saranno i focus delle UD successive. Qui costruiamo la base comune.

Risultato finale:

```text
frontend-products  → http://localhost:8118
backend-products   → http://localhost:8018
Prometheus         → http://localhost:9090
Grafana            → http://localhost:3000
Jaeger             → http://localhost:16686
```

---

## 1. Preparazione della cartella di lavoro

Copiare la cartella sorgente nel repository del partecipante:

```bash
mkdir -p work/UD18
cp -r UD18/src/app_products_local work/UD18/
cd work/UD18/app_products_local
```

Verificare la struttura:

```bash
find . -maxdepth 3 -type f | sort
```

Output atteso, in forma simile:

```text
./backend/app.py
./backend/Dockerfile
./backend/requirements.txt
./frontend/app.py
./frontend/Dockerfile
./frontend/requirements.txt
./docker-compose.yml
./prometheus/prometheus.yml
./grafana/provisioning/datasources/prometheus.yml
./scripts/start_stack_ud18.sh
./scripts/stop_stack_ud18.sh
./scripts/generate_traffic_ud18.sh
```

---

## 2. Verifica sintattica delle app

Prima di costruire immagini e container, verifichiamo almeno la sintassi Python:

```bash
python3 -m py_compile backend/app.py
python3 -m py_compile frontend/app.py
```

Se non compare output, la sintassi è valida.

---

## 3. Lettura rapida del docker-compose

Aprire:

```text
docker-compose.yml
```

Individuare i servizi:

```text
backend-products
frontend-products
prometheus
grafana
jaeger
```

Osservare soprattutto:

- porte pubblicate;
- `BACKEND_URL` del frontend;
- `OTEL_EXPORTER_OTLP_ENDPOINT`;
- volumi/configurazioni Prometheus e Grafana.

---

## 4. Avvio dello stack

Rendere eseguibili gli script:

```bash
chmod +x scripts/*.sh
```

Avviare:

```bash
./scripts/start_stack_ud18.sh
```

In alternativa:

```bash
docker compose up -d --build
```

Verificare:

```bash
docker compose ps
```

Tutti i servizi devono essere in stato `running` o equivalente.

---

## 5. Verifica applicativa frontend/backend

### 5.1 Frontend

```bash
curl -i http://localhost:8118/health
curl -i http://localhost:8118/ready
curl -i http://localhost:8118/version
curl -i http://localhost:8118/products
```

Risultati attesi:

| Endpoint | Atteso |
|---|---|
| `/health` | 200 |
| `/ready` | 200 e backend raggiungibile |
| `/version` | versione e ambiente |
| `/products` | catalogo prodotti |

### 5.2 Backend diretto

```bash
curl -i http://localhost:8018/health
curl -i http://localhost:8018/version
curl -i http://localhost:8018/api/products
```

Questa verifica serve a distinguere due problemi:

```text
backend non funziona
vs
frontend non riesce a raggiungere backend
```

---

## 6. Generazione traffico

Eseguire lo script:

```bash
./scripts/generate_traffic_ud18.sh
```

Lo script chiama endpoint normali, lenti ed errati:

```text
/products
/products/slow
/products/error
/ready
```

Questo traffico serve a popolare metriche, log e trace.

---

## 7. Verifica Prometheus

Aprire:

```text
http://localhost:9090/targets
```

Target attesi:

```text
products-backend   UP
products-frontend  UP
```

Provare alcune query nella pagina Graph:

```promql
up
```

```promql
app_http_requests_total
```

```promql
rate(app_http_requests_total[1m])
```

Non è necessario interpretare tutto ora: in UD19 entreremo nel dettaglio.

---

## 8. Verifica Grafana

Aprire:

```text
http://localhost:3000
```

Credenziali:

```text
admin / admin
```

Verificare:

```text
Connections / Data sources / Prometheus
```

Il datasource deve puntare a:

```text
http://prometheus:9090
```

Se Grafana chiede di cambiare password, si può saltare o impostare una password didattica temporanea.

---

## 9. Verifica Jaeger

Aprire:

```text
http://localhost:16686
```

Dopo aver generato traffico, cercare servizi come:

```text
products-frontend
products-backend
```

Se non compaiono subito, generare traffico di nuovo:

```bash
./scripts/generate_traffic_ud18.sh
```

Poi aggiornare la UI Jaeger.

---

## 10. Lettura log JSON

Leggere i log frontend:

```bash
docker compose logs --tail=80 frontend-products
```

Leggere i log backend:

```bash
docker compose logs --tail=80 backend-products
```

Cercare campi come:

```text
request_id
path
status
latency_ms
trace_id
span_id
```

Annotare un `request_id` presente su frontend e backend.

---

## 11. Simulazione errore controllato

```bash
curl -i http://localhost:8118/products/error
```

Verificare:

- risposta HTTP;
- log frontend;
- log backend;
- metriche Prometheus;
- eventuale trace Jaeger.

Non stiamo “rompendo” il laboratorio: stiamo producendo un segnale anomalo intenzionale.

---

## 12. Simulazione latenza controllata

```bash
curl -i http://localhost:8118/products/slow
```

Osservare:

- tempo percepito da curl;
- `latency_ms` nei log;
- durata dello span in Jaeger;
- metriche di durata in Prometheus.

---

## 13. Evidenze da raccogliere

Compilare:

```text
docs/template_evidence_ud18.md
```

E salvare una copia in:

```text
evidence/evidence_ud18_nome_cognome.md
```

Evidenze minime:

```text
[ ] docker compose ps
[ ] curl /health, /ready, /products
[ ] Prometheus targets UP
[ ] datasource Grafana Prometheus OK
[ ] Jaeger con servizi FE/BE visibili
[ ] log JSON con request_id
[ ] nota su /products/slow
[ ] nota su /products/error
```

---

## 14. Stop dello stack

A fine laboratorio:

```bash
./scripts/stop_stack_ud18.sh
```

Oppure:

```bash
docker compose down
```

Se vogliamo eliminare anche volumi temporanei:

```bash
docker compose down -v
```

Usare `-v` solo se non ci interessa conservare dati locali di Grafana.

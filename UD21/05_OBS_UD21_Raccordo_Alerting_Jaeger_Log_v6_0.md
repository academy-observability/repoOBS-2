# OBS UD21 — Raccordo operativo
# Dall'alert alle metriche, ai log e alle trace

## 1. L'alert è un punto di ingresso

Un alert non dimostra automaticamente la causa. La regola afferma che una condizione misurata è rimasta oltre soglia.

```text
Alert → conferma del sintomo → localizzazione → correlazione → conclusione
```

---

## 2. Error rate

Quando scatta `Products high error rate`:

1. verificare il valore della query A;
2. scomporre gli errori per `service`, `path`, `status`;
3. controllare log frontend e backend;
4. cercare request ID e trace ID;
5. usare Jaeger per seguire la chiamata distribuita.

Query di scomposizione:

```promql
sum by (service, path, status) (
  rate(app_http_requests_total{status=~"5.."}[1m])
)
```

---

## 3. Latenza p95

Quando scatta `Products high latency p95`:

1. verificare se il p95 è alto sul frontend;
2. confrontare path normali e `/products/slow`;
3. aprire Jaeger;
4. confrontare span frontend e backend;
5. stabilire dove viene trascorso il tempo.

L'alert fornisce una vista aggregata; Jaeger permette di osservare la durata di una singola richiesta distribuita.

---

## 4. Relazione con il webhook

Il payload webhook contiene:

- stato;
- label;
- annotazioni;
- valori della regola;
- collegamenti Grafana quando disponibili.

Non contiene automaticamente tutta la diagnosi. Il runbook trasforma questi metadati in una sequenza di indagine.

---

## 5. Nota sulla persistenza

Regole, metriche ed eventi webhook sono persistenti nei volumi della UD21. Le trace Jaeger sono invece in memoria e possono scomparire dopo la ricreazione del container.

Questa differenza insegna che la retention è una proprietà del backend di ciascun segnale, non dell'osservabilità in generale.

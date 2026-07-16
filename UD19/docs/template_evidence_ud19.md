# Evidence UD19 — Prometheus e Catalogo prodotti

## Dati partecipante

- Nome:
- Data:
- Repository:
- Cartella lavoro: `work/UD19/src/app_products_prometheus`

## 1. Stack avviato

Comando usato:

```bash
./scripts/start_stack_ud19.sh
```

Output/screenshot `docker compose ps`:

```text
INSERIRE OUTPUT
```

## 2. Target Prometheus

Prometheus URL:

```text
http://localhost:9090
```

| Job | Stato | Note |
|---|---|---|
| products-backend | | |
| products-frontend | | |
| prometheus | | |

## 3. Endpoint /metrics

Frontend:

```bash
curl -s http://localhost:8118/metrics | grep app_http | head
```

Backend:

```bash
curl -s http://localhost:8018/metrics | grep app_http | head
```

## 4. Query PromQL eseguite

| Query | Cosa ho osservato |
|---|---|
| `up` | |
| richieste totali | |
| request rate | |
| error rate | |
| latenza media | |
| p95 | |

## 5. Traffico generato

Comando:

```bash
./scripts/generate_traffic_ud19.sh
```

Oppure comando personalizzato:

```bash
INSERIRE COMANDO
```

## 6. Conclusione tecnica

Scrivere 5-8 righe:

```text
INSERIRE CONCLUSIONE
```

# Evidence UD18 — Stack locale Catalogo prodotti

## Dati partecipante

- Nome:
- Data:
- Repository:
- Cartella di lavoro:

## 1. Avvio stack

Comando usato:

```bash

```

Output/sintesi `docker compose ps`:

```text

```

## 2. Verifica applicativa

| Endpoint | Esito |
|---|---|
| `http://localhost:8118/health` | |
| `http://localhost:8118/ready` | |
| `http://localhost:8118/products` | |
| `http://localhost:8118/products/slow` | |
| `http://localhost:8118/products/error` | |

## 3. Prometheus

Target verificati in:

```text
http://localhost:9090/targets
```

| Target | Stato |
|---|---|
| products-backend | |
| products-frontend | |

Query provata:

```promql

```

## 4. Grafana

Datasource Prometheus verificato:

```text
Sì / No
```

Note:

```text

```

## 5. Jaeger

Servizi visibili:

```text

```

Trace osservata su endpoint:

```text

```

## 6. Log JSON

Esempio `request_id` osservato:

```text

```

Estratto log frontend:

```json

```

Estratto log backend:

```json

```

## 7. Interpretazione

Che cosa hai capito dal confronto tra `/products`, `/products/slow` e `/products/error`?

```text

```

## 8. Problemi incontrati

```text

```

## 9. Cleanup

Comando usato:

```bash

```

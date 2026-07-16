# OBS UD19 — Laboratorio autonomo
# PromQL su traffico, errori e latenza del Catalogo prodotti

## Scenario

Il docente ti chiede di dimostrare che sai usare Prometheus non solo per vedere target UP/DOWN, ma per leggere il comportamento dell'app prodotti.

Devi produrre una breve evidenza tecnica con query, output e interpretazione.

## Attività

1. Avvia lo stack UD19.
2. Apri Prometheus.
3. Verifica target `products-backend` e `products-frontend`.
4. Genera traffico normale:

```bash
for i in {1..30}; do curl -s -o /dev/null http://localhost:8118/products; done
```

5. Genera traffico lento:

```bash
for i in {1..10}; do curl -s -o /dev/null http://localhost:8118/products/slow; done
```

6. Genera errori controllati:

```bash
for i in {1..8}; do curl -s -o /dev/null http://localhost:8118/products/error || true; done
```

7. Esegui almeno cinque query PromQL:
   - `up`;
   - richieste totali;
   - request rate;
   - error rate;
   - latenza media o p95.

8. Salva le evidenze in `docs/evidence_ud19.md`.

## Criteri di accettazione

Il lavoro è valido se dimostri:

- target Prometheus UP;
- metriche applicative presenti;
- aumento dei counter dopo il traffico;
- presenza di errori dopo `/products/error`;
- differenza di latenza tra `/products` e `/products/slow`;
- interpretazione scritta, non solo screenshot.

## Domanda finale

Scrivi una risposta breve:

```text
Quale metrica useresti come base per una dashboard Grafana e quale come base per un alert?
```

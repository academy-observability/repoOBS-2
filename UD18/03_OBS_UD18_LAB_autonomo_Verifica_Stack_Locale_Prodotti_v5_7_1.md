# OBS UD18 — Laboratorio autonomo
# Verifica controllata dello stack locale Catalogo prodotti

## Scenario

Hai ricevuto uno stack locale già predisposto. Devi dimostrare che l'applicazione e gli strumenti osservanti funzionano e che sai raccogliere evidenze minime.

## Attività

1. Avvia lo stack con Docker Compose.
2. Verifica frontend e backend.
3. Genera traffico normale, lento ed errato.
4. Verifica Prometheus targets.
5. Verifica datasource Grafana.
6. Verifica presenza servizi/tracce in Jaeger.
7. Leggi log JSON frontend e backend.
8. Compila un report evidenze.

## Comandi minimi

```bash
cd work/UD18/app_products_local
docker compose up -d --build
docker compose ps
curl -i http://localhost:8118/ready
curl -i http://localhost:8118/products
curl -i http://localhost:8118/products/slow
curl -i http://localhost:8118/products/error
```

## Evidenze richieste

| Evidenza | Come dimostrarla |
|---|---|
| Stack avviato | output `docker compose ps` |
| Frontend pronto | output `/ready` |
| Catalogo visibile | output `/products` o screenshot browser |
| Prometheus target UP | screenshot o nota da `/targets` |
| Grafana datasource | screenshot o descrizione |
| Jaeger trace | screenshot o nome servizi visibili |
| Log correlabili | estratto con `request_id` |

## Domanda finale

Spiega in massimo 10 righe perché uno stack locale come questo aiuta a capire meglio l'observability cloud vista in UD17.

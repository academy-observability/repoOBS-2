# OBS UD18 — Mini-attività
# Mappa app-stack / obs-stack sul Catalogo prodotti

## Obiettivo

Completare una mappa ragionata dello stack locale UD18. Non è un esercizio di memoria: serve a verificare che siano chiari confini, porte, nomi, segnali e responsabilità.

## 1. Tabella componenti

Compila la tabella.

| Componente | App-stack o obs-stack? | Porta host | Porta interna | Responsabilità |
|---|---|---:|---:|---|
| frontend-products | | | | |
| backend-products | | | | |
| prometheus | | | | |
| grafana | | | | |
| jaeger | | | | |

## 2. Comunicazione FE → BE

Completa:

```text
Il frontend raggiunge il backend usando l'URL: ____________________________
```

Spiega perché non deve usare `localhost:8018`.

## 3. Segnali osservabili

Per ogni segnale indica chi lo produce e chi lo legge.

| Segnale | Prodotto da | Letto da |
|---|---|---|
| metriche `/metrics` | | |
| log JSON | | |
| trace OTLP | | |
| dashboard | | |

## 4. Endpoint osservabili

Associa ogni endpoint al suo uso.

| Endpoint | Uso |
|---|---|
| `/products` | |
| `/products/slow` | |
| `/products/error` | |
| `/ready` | |
| `/metrics` | |

## 5. Domande brevi

1. Quale componente raccoglie metriche?
2. Quale componente visualizza metriche?
3. Quale componente mostra trace distribuite?
4. Quale campo permette di correlare log frontend e backend?
5. Quale URL apriamo per verificare i target Prometheus?
6. Quale URL apriamo per Jaeger?
7. Che differenza c'è tra porta host e porta container?
8. Perché UD18 è il ponte verso UD19–UD22?

## 6. Risposta libera

Scrivi in 5-8 righe cosa succede quando chiami:

```bash
curl http://localhost:8118/products
```

Devi citare almeno: frontend, backend, `BACKEND_URL`, log, metriche e trace.

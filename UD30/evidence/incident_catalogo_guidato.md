# Evidence packet — Incidente Catalogo prodotti

## Scenario

Il team segnala rallentamenti e alcuni errori nell’endpoint che restituisce il Catalogo prodotti.

## Finestra temporale

25 luglio 2026, dalle 14:30 alle 14:50.

## Sintomi osservati

- alcuni utenti segnalano caricamenti lenti;
- una parte delle richieste termina con errore HTTP 500;
- il problema non era visibile nella finestra 14:00–14:20.

## Metriche

- p95 di `/api/products`: da circa 420 ms a 1.840 ms;
- error rate: da 0,5% a 6,8%;
- traffico: sostanzialmente stabile;
- CPU del backend: dal 42% al 49%;
- memoria del backend: stabile.

## Log significativo

```text
14:36:18 ERROR products.repository query timeout after 1500 ms
request_id=req-8432 endpoint=/api/products
```

## Trace significativo

Durata totale richiesta: 1.720 ms.

```text
frontend request                 1.720 ms
└── backend /api/products       1.610 ms
    ├── auth check                 18 ms
    ├── product-service            95 ms
    └── database SELECT         1.350 ms
```

Il trace rappresenta una singola richiesta lenta, non tutte le richieste.

## Modifiche recenti

- versione `products-backend 2.4` distribuita alle 14:25;
- la release include modifiche al filtro per categoria;
- non è stato ancora eseguito un rollback.

## Informazioni non disponibili

- CPU, memoria e I/O del database;
- numero di connessioni nel pool;
- piano di esecuzione della query;
- confronto sistematico tra trace prima e dopo la release;
- comportamento dopo rollback;
- percentuale di errori per categoria richiesta.

## Vincolo

Le evidenze mostrano un degrado e un’attesa importante sul database. Non dimostrano ancora una root cause definitiva.

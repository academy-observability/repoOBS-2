# Evidence packet — Incidente Checkout

## Scenario

Durante una campagna promozionale alcuni utenti non riescono a completare l’ordine. Il team deve preparare un handoff per il turno successivo.

## Finestra temporale

25 luglio 2026, dalle 17:05 alle 17:30.

## Sintomi

- aumento dei tempi di conferma ordine;
- alcuni errori HTTP 502 sul Checkout;
- il carrello continua a funzionare normalmente.

## Metriche

- p95 `/api/checkout`: da 780 ms a 2.450 ms;
- error rate Checkout: da 0,8% a 4,9%;
- traffico Checkout: +18% rispetto alla media dell’ora precedente;
- CPU servizio Checkout: 54%, senza picchi anomali;
- richieste al provider pagamenti: +19%.

## Log

```text
17:18:44 WARN payment-client upstream response timeout
request_id=chk-2918 timeout_ms=2000 attempt=1
```

## Trace

Durata totale: 2.380 ms.

```text
checkout request                2.380 ms
├── cart validation                42 ms
├── inventory reservation         130 ms
└── payment provider            2.110 ms
```

## Modifiche recenti

- nessuna release del Checkout nelle ultime 24 ore;
- alle 16:55 è stata modificata la configurazione del timeout del payment client da 3.000 ms a 2.000 ms;
- il provider pagamenti non ha ancora confermato un incidente.

## Informazioni mancanti

- latenza del provider pagamenti vista da altri clienti;
- percentuale di retry riusciti;
- distribuzione geografica degli errori;
- esito del ripristino del timeout precedente;
- stato della rete in uscita;
- dettaglio degli status restituiti dal provider.

## Nota fallback

Se Ollama non è disponibile usare:

```text
fallback/risposta_autonomo_llama3_2_1b.md
datasets/fallback_autonomous_telemetry.csv
```

# Evidence packet — Checkout

## Finestra

`15:20–15:35`

## Evidenze

- **A1 — Metriche**: p95 endpoint `/checkout` passa da 420 ms a 1.480 ms.
- **A2 — Traffico**: richieste al minuto stabili entro ±5% rispetto alla baseline.
- **A3 — Errori**: HTTP 5xx resta sotto 0,8%; aumentano invece i timeout lato client.
- **A4 — Trace**: in `trace-pay-031`, checkout totale 1.620 ms; chiamata `payment-service` 980 ms; chiamata `inventory-service` 210 ms.
- **A5 — Log payment**: tre messaggi `provider response delayed`; nessun errore di autenticazione.
- **A6 — Release**: nessuna nuova release checkout o payment nelle ultime quattro ore.
- **A7 — Limite**: non sono disponibili metriche del provider esterno né un confronto completo per regione.

## Regola

Non presentare il provider esterno come root cause certa. Il trace e i log lo rendono una ipotesi prioritaria, ma mancano metriche dirette e confronto regionale.

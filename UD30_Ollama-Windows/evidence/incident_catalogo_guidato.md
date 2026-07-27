# Evidence packet — Catalogo prodotti

## Finestra

`10:00–10:15`

## Evidenze

- **E1 — Metriche**: p95 frontend `/products` ≈ 510 ms; p95 backend `/api/products` ≈ 180 ms.
- **E2 — Errori**: error rate frontend 2,1%; backend 0,4%.
- **E3 — Release**: nuova release frontend completata alle 09:42; nessuna release backend nella finestra precedente.
- **E4 — Trace**: `trace-cat-017`, durata frontend 535 ms; chiamata backend 145 ms; tempo restante non attribuito dal trace disponibile.
- **E5 — Architettura**: il laboratorio non usa un database applicativo per il Catalogo prodotti.
- **E6 — Limite**: non sono stati analizzati tutti i log frontend, né tutti i trace lenti della finestra.

## Regola

Ogni affermazione importante deve essere collegata a una o più evidenze. La release è un indizio temporale, non una causa dimostrata.

# OBS UD20 — Laboratorio autonomo
# Dashboard operativa per il Catalogo prodotti

## Scenario

Il team vuole una dashboard leggermente più operativa rispetto a quella base. Devi partire dalla dashboard UD20 e aggiungere almeno due elementi utili per la diagnosi.

## Attività

1. Avvia lo stack UD20.
2. Genera traffico con almeno 80 round:

```bash
ROUNDS=80 ./scripts/generate_traffic_ud20.sh
```

3. Duplica o modifica la dashboard esistente.
4. Aggiungi almeno due pannelli tra:
   - richieste solo frontend;
   - richieste solo backend;
   - errori per path;
   - latenza media per path;
   - confronto `/products` vs `/products/slow`;
   - tabella totale richieste per status.
5. Dai a ogni pannello un titolo comprensibile.
6. Scrivi in `docs/evidence_ud20.md` perché quei pannelli sono utili.

## Vincoli

- La dashboard deve usare Prometheus come datasource.
- Le query devono essere PromQL reali.
- Devi usare traffico normale, lento ed errore.
- Non basta uno screenshot: devi spiegare che cosa si vede.

## Output atteso

```text
Dashboard Grafana modificata
Query PromQL documentate
Evidenza su traffico normale/lento/errore
Breve interpretazione tecnica
```

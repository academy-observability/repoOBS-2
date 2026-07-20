# OBS UD22 — Laboratorio autonomo
# Mini incident investigation con Jaeger

## Scenario

Gli utenti segnalano che il Catalogo prodotti presenta comportamenti non uniformi: alcune richieste sono regolari, una è molto lenta e una restituisce un errore.

Il compito non consiste nel modificare lo stack. Dobbiamo ricostruire il comportamento usando evidenze osservabili.

## Task 1 — Generazione del caso

```bash
cd UD22/src/app_products_tracing
./scripts/generate_incident_case_ud22.sh
```

Lo script produce otto `request_id` senza indicare nella consegna quale richiesta sia lenta o in errore.

## Task 2 — Ricerca in Jaeger

In Jaeger:

1. selezionare `products-frontend`;
2. cercare le trace recenti;
3. confrontare durata e stato;
4. individuare la trace lenta;
5. individuare la trace in errore;
6. annotare i rispettivi `trace_id`.

## Task 3 — Analisi della trace lenta

Documentare:

- durata totale;
- span dominante;
- servizio responsabile;
- relazione tra client span e server span;
- conclusione tecnica.

## Task 4 — Analisi della trace in errore

Documentare:

- status osservato;
- span in cui nasce l'errore;
- attributo applicativo rilevante;
- modalità con cui l'errore si propaga al frontend.

## Task 5 — Conferma tramite log

Per ciascun `request_id` individuato:

```bash
./scripts/show_correlated_logs_ud22.sh REQUEST_ID
```

Confermare che i log frontend e backend condividano `request_id` e `trace_id`.

## Task 6 — Incident record

Compilare `docs/template_incident_record_ud22.md`.

La conclusione deve distinguere chiaramente:

```text
sintomo aggregato
richiesta rappresentativa
servizio coinvolto
span determinante
evidenza di log
azione successiva
```

Non è richiesto modificare il codice né il Docker Compose.

# OBS UD21 — Mini-attività
# Progettare una regola prima di crearla

## Scenario

Il team vuole ricevere una notifica quando gli utenti del frontend incontrano una quota anomala di errori sugli endpoint products.

Prima di aprire Grafana, completare la scheda.

| Campo | Decisione |
|---|---|
| Punto di vista del segnale | |
| Metrica | |
| Filtri label | |
| Query o descrizione della query | |
| Soglia | |
| Evaluation interval | |
| Pending period | |
| Folder | |
| Evaluation group | |
| Contact point | |
| Labels operative | |
| Summary | |
| Prima verifica del runbook | |
| Dato che deve persistere dopo restart | |

## Domande

1. Perché non sommiamo indiscriminatamente frontend e backend nel rapporto user-facing?
2. Quale problema produce `0 / 0` quando non esiste traffico?
3. Qual è la differenza tra query A e threshold B?
4. Perché B deve essere impostata come alert condition?
5. Qual è la differenza tra evaluation interval e pending period?
6. Che cosa prova il test del contact point e che cosa non prova?
7. Perché è importante ricevere anche il messaggio `resolved`?
8. Quali dati perderemmo senza il volume Grafana?
9. Perché `docker compose down` e `docker compose down -v` non sono equivalenti?

## Consegna

Salvare le risposte nel report e confrontarle con la soluzione docente solo dopo il completamento.

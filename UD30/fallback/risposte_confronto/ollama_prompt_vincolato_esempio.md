# Risposta Ollama locale di esempio — prompt vincolato

## Fatti osservati

- La latenza p95 e gli errori sono aumentati.
- Il traffico è stabile.
- Una query ha raggiunto il timeout.
- Il database occupa 1.350 ms nel trace.
- È stata rilasciata la versione 2.4 poco prima del problema.

## Ipotesi

1. Il nuovo filtro potrebbe aver modificato la query e rallentato il database.
2. Il database potrebbe essere sovraccarico.

## Evidenze

La prima ipotesi è compatibile con la release e con il trace. La seconda è compatibile con il timeout, ma non ci sono metriche CPU o I/O.

## Informazioni mancanti

Metriche del database, pool connessioni, query effettiva e prova di rollback.

## Verifiche

- confrontare la query con la versione precedente;
- controllare CPU, I/O e connessioni;
- provare il rollback;
- analizzare più trace.

## Certezza

Media: il database è coinvolto, ma non è possibile stabilire con certezza la causa.

## Nota didattica

La struttura è adeguata. La frase “il database è coinvolto” va interpretata come contributo osservato alla latenza, non come dimostrazione che il problema risieda necessariamente nell’infrastruttura database.

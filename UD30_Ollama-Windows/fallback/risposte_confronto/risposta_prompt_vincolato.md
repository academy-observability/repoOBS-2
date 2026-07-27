# Risposta simulata — prompt vincolato

## Fatti osservati

- Il p95 frontend è circa 510 ms e quello backend circa 180 ms [E1].
- Nel trace disponibile, il frontend dura 535 ms e la chiamata backend 145 ms [E4].
- Una release frontend è terminata alle 09:42 [E3].
- Il Catalogo del laboratorio non usa un database applicativo [E5].

## Inferenze

- Nel trace disponibile, una parte consistente della durata non è attribuita alla chiamata backend [E1, E4].

## Ipotesi

- Il degrado potrebbe trovarsi nel frontend o in una dipendenza non visibile nel trace disponibile.
- La release potrebbe essere correlata temporalmente, ma non è dimostrato che sia la causa [E3, E6].

## Informazioni mancanti

- log frontend completi;
- altri trace lenti;
- confronto tra release precedente e attuale.

## Verifiche

1. Analizzare i log frontend nella finestra.
2. Confrontare trace lenti e normali.
3. Eseguire un confronto controllato tra versioni o rollback, se operativo e a basso rischio.

## Limite

La root cause non è dimostrata.

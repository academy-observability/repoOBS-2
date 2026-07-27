# Risposta fallback — incidente Checkout

## Fatti osservati

- Il p95 del Checkout è aumentato a 2.450 ms e l’error rate al 4,9%.
- Il traffico è aumentato del 18%.
- Nel trace il provider pagamenti usa 2.110 ms su 2.380 ms.
- Il client registra un timeout a 2.000 ms.
- Il timeout è stato ridotto da 3.000 a 2.000 ms alle 16:55.

## Ipotesi

1. La nuova soglia di timeout trasforma risposte lente del provider in errori 502.
2. Il provider pagamenti sta subendo un degrado coincidente con l’aumento del traffico.
3. La rete in uscita verso il provider è degradata.

## Informazioni mancanti

Status dettagliati del provider, retry, latenza osservata da altri client, rete in uscita ed esito del ripristino del timeout.

## Verifiche

1. Ripristinare in modo controllato il timeout precedente e misurare errori e latenza.
2. Separare timeout client da errori restituiti dal provider.
3. Verificare retry e stato della rete.
4. Chiedere conferma al provider.

## Certezza

Media: la modifica del timeout è temporalmente e tecnicamente compatibile con gli errori, ma non esclude un degrado del provider.

# Risposta cloud di esempio — prompt vincolato

## 1. Fatti osservati

- Tra le 14:30 e le 14:50 il p95 di `/api/products` è aumentato da circa 420 ms a 1.840 ms.
- L’error rate è aumentato dallo 0,5% al 6,8% con traffico sostanzialmente stabile.
- Un log riporta un timeout di query dopo 1.500 ms.
- Nel trace disponibile, la SELECT sul database dura 1.350 ms su 1.720 ms complessivi.
- La versione 2.4 è stata distribuita alle 14:25 e include modifiche al filtro per categoria.

## 2. Ipotesi ordinate per plausibilità

1. Una modifica applicativa o di query collegata al nuovo filtro ha aumentato il tempo della SELECT.
2. Il database o il pool di connessioni è in una condizione di saturazione indipendente dalla release.
3. Il trace osservato rappresenta un caso isolato e il degrado aggregato può dipendere anche da altri percorsi.

## 3. Evidenze a supporto

L’ipotesi 1 è sostenuta dalla vicinanza temporale della release e dalla durata elevata della SELECT, ma non è dimostrata. L’ipotesi 2 è compatibile con il timeout, ma mancano metriche del database e del pool. L’ipotesi 3 resta possibile perché è disponibile un solo trace lento.

## 4. Informazioni mancanti

Metriche CPU/I/O del database, pool connessioni, piano di esecuzione, confronto di più trace prima e dopo la release, comportamento dopo rollback.

## 5. Verifiche successive

1. Confrontare distribuzione e p95 degli span database prima e dopo la release.
2. Analizzare query e piano di esecuzione del filtro per categoria.
3. Acquisire metriche database e pool connessioni.
4. Eseguire rollback o canary controllato e confrontare i risultati.

## 6. Livello di certezza

Medio-basso: il database è il principale contributore nel trace osservato, ma la root cause non è ancora dimostrata.

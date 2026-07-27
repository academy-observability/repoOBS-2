# Mini-attività — Fatti, ipotesi e verifiche

## Durata

45 minuti con review.

## Scenario

Usare `evidence/incident_catalogo_guidato.md`.

## Attività 1

Classificare le frasi:

1. Il p95 frontend è superiore al p95 backend.
2. Il database è saturo.
3. Nel trace disponibile la chiamata backend dura 145 ms.
4. La release ha certamente causato il problema.
5. Occorre analizzare i log frontend della finestra.
6. Il degrado potrebbe trovarsi nel frontend o in una dipendenza non visibile nel trace disponibile.

Categorie:

```text
fatto | inferenza | ipotesi | verifica | claim non supportato
```

## Attività 2

Compilare `templates/matrice_claim_evidence.md` con almeno cinque claim.

## Attività 3

Riscrivere questa conclusione:

> Il nuovo rilascio ha rotto il database e deve essere immediatamente annullato.

La nuova versione deve:

- usare soltanto evidenze disponibili;
- dichiarare l'incertezza;
- proporre una verifica a basso rischio;
- non inventare componenti.

## Output

```text
outputs/mini_attivita_claim_evidence.md
```

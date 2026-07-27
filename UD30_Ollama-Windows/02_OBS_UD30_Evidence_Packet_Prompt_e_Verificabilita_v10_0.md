# UD30 — Evidence packet, prompt e verificabilità

## 1. Evidence packet

Un LLM non vede automaticamente il sistema. Riceve il contesto che gli viene fornito.

Un evidence packet contiene un insieme controllato di:

- metriche;
- anomaly candidate;
- output ML;
- trace;
- informazioni architetturali;
- limiti dei dati disponibili.

Ogni evidenza deve avere un identificatore, per esempio `E1`, `E2`, `E3`.

## 2. Quattro categorie operative

| Categoria | Significato |
|---|---|
| Fatto | direttamente supportato da una evidenza |
| Inferenza | conclusione ragionevole ottenuta combinando fatti |
| Ipotesi | spiegazione possibile da verificare |
| Claim non supportato | affermazione senza evidenza disponibile |

## 3. Prompt aperto

Un prompt aperto può essere:

```text
Analizza l'incidente e indica la causa più probabile.
```

Il rischio è che il modello completi i vuoti con dettagli plausibili.

## 4. Prompt vincolato

Un prompt vincolato definisce:

- dati ammessi;
- struttura dell'output;
- obbligo di citare le evidenze;
- distinzione fatti/ipotesi;
- divieto di inventare componenti;
- richiesta di informazioni mancanti e verifiche.

```text
Usa esclusivamente E1–E6.
Per ogni fatto cita gli ID.
Se una causa non è dimostrata, chiamala ipotesi.
```

## 5. Claim–evidence mapping

| Claim | Tipo | Evidenze | Valutazione |
|---|---|---|---|
| Il frontend contribuisce più del backend alla durata del trace | inferenza | E1, E4 | supportato |
| Il database è saturo | claim | nessuna | non supportato |
| La release potrebbe essere correlata | ipotesi | E3 | da verificare |

## 6. Correlazione e causalità

```text
A accade prima di B
≠
A causa B
```

Una release precedente al degrado è un indizio temporale. Per sostenere causalità servono confronti, rollback, differenze di versione, trace o altre evidenze.

## 7. Handoff verificabile

Un handoff tecnico utile contiene:

1. sintesi;
2. fatti osservati con ID;
3. ipotesi ordinate;
4. informazioni mancanti;
5. verifiche consigliate;
6. azioni a basso rischio;
7. livello di confidenza motivato.

## Regola conclusiva

```text
LLM utile
=
output leggibile + provenienza + limiti + verifiche
```

Non basta ottenere una risposta elegante.

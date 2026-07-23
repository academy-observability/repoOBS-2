# UD28 — Potenziamento opzionale pratico v1.0

## Scopo

Il laboratorio principale della UD28 resta invariato.

Questo blocco è facoltativo e serve a consolidare, con maggiore autonomia, il salto concettuale della UD28:

```text
baseline
→ soglia esplicita
→ detection
→ confronto con reference
→ valutazione degli errori
```

La progressione è:

```text
ATTIVITÀ 1 — guidata
sensibilità al moltiplicatore
        ↓
ATTIVITÀ 2 — parzialmente guidata
confronto sistematico di più soglie
        ↓
ATTIVITÀ 3 — specifiche + struttura minima
analisi dei casi FP e FN
        ↓
ATTIVITÀ 4 — maggiore autonomia
stabilità della baseline
        ↓
CHALLENGE
report integrato sul detector statistico
```

## Tempo di lavoro previsto

| Blocco | Lavoro partecipanti |
|---|---:|
| Briefing iniziale | 15–20 min |
| Attività 1 — sensibilità soglia | 30–40 min |
| Attività 2 — confronto multipli | 35–45 min |
| Attività 3 — error analysis | 40–50 min |
| Attività 4 — stabilità baseline | 45–55 min |
| Challenge integrativa | 55–70 min |
| Revisione finale | 15–20 min |

Totale realistico:

```text
circa 3h55 – 5h00
```

## Regola sul codice di servizio

Negli starter alcune parti sono già fornite e marcate:

```python
# CODICE DI SERVIZIO
```

Servono a evitare che il focus si sposti su dettagli tecnici già secondari rispetto all'obiettivo della UD.

Il codice di servizio va comunque letto e spiegato.

## Concetti riutilizzati

- DataFrame, filtri, funzioni, cicli;
- mediana e MAD;
- baseline;
- soglia esplicita;
- prediction;
- reference label;
- TP, FP, FN, TN;
- precision e recall.

## Concetti volutamente esclusi

Non introduciamo:

- training;
- modello addestrato;
- feature engineering;
- classificatori ML;
- decision tree;
- inferenza ML.

La domanda resta:

> Quanto è affidabile una regola statistica esplicita e come cambiano i suoi errori quando cambiamo le scelte del detector o la baseline?

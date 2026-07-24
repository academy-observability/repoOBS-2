# UD29 — Potenziamento opzionale pratico v1.0

## Scopo

Il percorso principale della UD29 resta centrato su un solo salto concettuale:

```text
regola definita da noi
        ↓
regola appresa dagli esempi durante fit()
```

Questo blocco facoltativo consolida lo stesso concetto con più autonomia, senza introdurre nuovi algoritmi, feature engineering avanzato o MLOps.

La progressione è:

```text
ATTIVITÀ 1
soglia appresa ≠ regola HTTP
        ↓
ATTIVITÀ 2
quanto conta la copertura del training
        ↓
ATTIVITÀ 3
error analysis delle prediction
        ↓
ATTIVITÀ 4
percorsi decisionali spiegabili
        ↓
CHALLENGE
audit integrato del modello
```

## Tempo di lavoro previsto

| Blocco | Lavoro partecipanti |
|---|---:|
| Briefing e lettura consegne | 15–20 min |
| Attività 1 — sondare casi non visti | 30–40 min |
| Attività 2 — copertura del training | 35–45 min |
| Attività 3 — error analysis | 40–50 min |
| Attività 4 — percorsi decisionali | 40–50 min |
| Challenge — audit spiegabile | 55–70 min |
| Revisione finale | 15–20 min |

Totale realistico:

```text
circa 3h50 – 4h55
```

## Regola sul codice di servizio

Le parti marcate:

```python
# CODICE DI SERVIZIO
```

sono già fornite perché non costituiscono il nuovo obiettivo didattico. Devono essere lette e comprese, ma non necessariamente riscritte.

Esempi:

- percorsi con `Path`;
- caricamento e salvataggio CSV;
- `merge` tra prediction e reference;
- uso di `export_text`;
- uso tecnico di `decision_path`;
- calcolo ripetitivo delle metriche.

## Concetti consolidati

- `fit()` come apprendimento;
- `predict()` come inferenza;
- feature e target;
- training/test/reference separati;
- Decision Tree leggibile;
- TP, FP, FN, TN, precision, recall;
- limite delle feature disponibili;
- distinzione tra regola appresa e conoscenza del dominio.

## Concetti volutamente esclusi

Non introduciamo:

- Random Forest o altri algoritmi;
- reti neurali;
- GridSearch o cross-validation;
- feature engineering avanzato;
- MLOps;
- AI generativa.

La domanda resta:

> Che cosa ha realmente appreso il modello dai dati disponibili, che cosa non può sapere e come possiamo verificarlo?

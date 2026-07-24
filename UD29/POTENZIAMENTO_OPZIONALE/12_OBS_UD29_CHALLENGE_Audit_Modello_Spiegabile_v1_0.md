# Challenge finale — Audit di un modello spiegabile

## Livello

**Autonomo con codice di servizio fornito**

Tempo indicativo: **55–70 minuti**.

## Scenario

Un collega presenta il Decision Tree come segue:

> “Il modello ha precision 1,00, quindi le sue regole descrivono correttamente il comportamento del servizio.”

Devi produrre un audit tecnico che distingua:

```text
regole apprese
metriche
errori residui
limiti delle feature
conoscenza del dominio
```

## Starter

```bash
cp POTENZIAMENTO_OPZIONALE/src/starter/05_model_audit_CHALLENGE.py \
   POTENZIAMENTO_OPZIONALE/src/05_model_audit.py
```

## Output richiesti

### A. `model_rules.txt`

Regole testuali apprese dal Decision Tree.

### B. `evaluation_summary.csv`

Una riga con:

```text
TP FP FN TN precision recall
```

### C. `misclassified_cases.csv`

I casi in cui prediction e reference differiscono.

### D. `synthetic_probe.csv`

Quattro casi con stessa durata e status:

```text
200
300
404
500
```

### E. Conclusioni

Compilare:

```text
POTENZIAMENTO_OPZIONALE/templates/conclusioni_audit_modello.md
```

con:

- 3 affermazioni supportate dai risultati;
- 2 limiti del modello;
- 1 spiegazione di `status_code <= 350`;
- 1 motivo per cui precision 1,00 non significa “modello perfetto”;
- 2 evidenze aggiuntive che potrebbero essere utili in un caso reale.

## Vincoli

Non introdurre:

- nuovi algoritmi;
- nuove feature costruite ad hoc;
- tuning avanzato.

L'audit deve riguardare il modello già studiato e ciò che possiamo realmente dedurre dalle evidenze disponibili.

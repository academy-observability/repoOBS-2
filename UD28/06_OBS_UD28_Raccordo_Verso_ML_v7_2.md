# UD28 — Raccordo verso UD29

Abbiamo costruito un detector con una regola scritta da noi:

```text
se duration_ms > soglia
→ anomaly
```

Abbiamo scoperto due limiti:

```text
1. usa una sola feature
2. la regola è scelta manualmente
```

Il falso negativo `eval-005` rende il primo limite molto concreto:

```text
duration_ms non supera la soglia
ma status_code = 500
```

La domanda della UD29 sarà:

> Possiamo costruire un modello che apprenda dai dati come combinare più caratteristiche?

```text
UD28
regola definita da noi
        ↓
UD29
regola appresa dai dati
```

Prima di arrivare al ML, però, dobbiamo conservare ciò che abbiamo imparato:

- prediction non significa verità;
- ground truth deve avere provenienza e motivazione;
- un modello deve essere valutato su casi che non usa per “darsi ragione”.

# UD29 — Laboratorio autonomo
# Quanto conta la scelta delle feature?

## Obiettivo

Usare lo **stesso Decision Tree** con due configurazioni:

```text
MODELLO A
feature = duration_ms

MODELLO B
feature = duration_ms + status_code
```

Non introduciamo un nuovo algoritmo.

Verifichiamo quanto conta l'informazione disponibile.

## Dati usati

```text
ml_training_labeled.csv
→ fit

ml_test_features.csv
→ predict

ml_test_reference_labels.csv
→ valutazione successiva
```

Il reference file non è una feature del modello.

## Starter

Linux / WSL:

```bash
cp src/starter/compare_feature_sets_TODO.py src/compare_feature_sets.py
```

PowerShell:

```powershell
Copy-Item src/starter/compare_feature_sets_TODO.py src/compare_feature_sets.py
```

## TODO

Completare:

1. `FEATURES_A` con `duration_ms`;
2. `FEATURES_B` con `duration_ms` e `status_code`;
3. eseguire entrambi i modelli;
4. confrontare TP/FP/FN/TN, precision e recall.

## Domande

1. Quale configurazione trova più anomaly?
2. Quale informazione aggiunge `status_code`?
3. Il modello con due feature diventa perfetto?
4. Perché alcune anomaly possono restare difficili da rilevare?
5. Perché `reference_label` non compare in `FEATURES_A` o `FEATURES_B`?

## Vincoli

Non cambiare:

- algoritmo;
- `max_depth=2`;
- dataset.

L'unica variabile dell'esperimento deve essere **l'insieme delle feature**.

## Competenza verificata

> So spiegare che il modello predice usando solo le feature e che la reference serve successivamente per misurare la qualità della prediction.

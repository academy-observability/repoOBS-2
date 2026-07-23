# UD28 — Guida operativa

## Ambiente

Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ordine degli script

```bash
python src/01_build_threshold.py
python src/02_detect_candidates.py
python src/03_inspect_reference_labels.py
python src/04_compare_prediction_reference.py
python src/05_evaluate_detector.py
python src/06_compare_two_thresholds.py
```

## File prodotti

```text
outputs/predictions.csv
outputs/comparison.csv
```

## Regola importante

Non aprire `products_reference_labels.csv` per “aiutare” il detector prima di aver generato `predictions.csv`.

L'ordine didattico è intenzionale:

```text
prediction prima
reference dopo
```

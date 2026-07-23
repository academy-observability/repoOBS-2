# Script UD28

Ordine:

1. `01_build_threshold.py`
2. `02_detect_candidates.py`
3. `03_inspect_reference_labels.py`
4. `04_compare_prediction_reference.py`
5. `05_evaluate_detector.py`
6. `06_compare_two_thresholds.py`

## Confine

Il detector della UD28 usa intenzionalmente una sola feature: `duration_ms`.

La reference viene consultata soltanto dopo aver prodotto le prediction.

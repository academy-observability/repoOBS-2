# Script UD29

Ordine consigliato:

1. `01_learning_from_examples.py` — rende visibile l'apprendimento su toy dataset;
2. `02_features_and_target.py` — feature X e target y;
3. `03_train_decision_tree.py` — training completo con `fit()`;
4. `04_predict_test.py` — inferenza su test senza label;
5. `05_evaluate_model.py` — confronto con reference separata;
6. `06_read_tree_rules.py` — lettura delle regole apprese;
7. `07_compare_depths.py` — overfitting intuitivo;
8. `starter/compare_feature_sets_TODO.py` — laboratorio autonomo.

## Idea centrale

```text
fit()     → apprende
predict() → applica ciò che è stato appreso
```

Le parti marcate `CODICE DI SERVIZIO` aiutano l'esecuzione ma non sono il nuovo obiettivo didattico.

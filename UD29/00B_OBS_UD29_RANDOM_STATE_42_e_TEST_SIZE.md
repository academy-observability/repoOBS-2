# UD29 — Che cosa significa `random_state=42`

## Perché compare spesso il numero 42 nel Machine Learning

Nel codice di Machine Learning possiamo incontrare istruzioni come:

```python
DecisionTreeClassifier(
    max_depth=2,
    random_state=42
)
```

oppure:

```python
train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

La domanda è:

> **Che cosa significa `42` e perché viene usato?**

---

# 1. `42` è un seme per la casualità

Molti algoritmi e molte operazioni di Machine Learning utilizzano elementi casuali.

`random_state=42` serve a fissare il **seme**, cioè il punto di partenza del generatore pseudo-casuale.

In forma semplice:

```text
random_state=42
        ↓
stesso punto di partenza
        ↓
stesse scelte pseudo-casuali
        ↓
risultati riproducibili
```

Il numero `42` non ha un significato matematico speciale.

Potremmo scrivere anche:

```python
random_state=1
random_state=10
random_state=123
```

Ciò che conta è usare sempre lo stesso valore quando vogliamo ripetere lo stesso esperimento.

---

# 2. Perché proprio 42?

`42` è diventato un valore molto usato negli esempi di programmazione e Machine Learning.

È una convenzione.

Non significa:

```text
42 = valore migliore per il modello
```

Significa soltanto:

```text
42 = un valore scelto come seme fisso
```

Quindi:

> **42 non migliora il modello: rende l'esperimento riproducibile.**

---

# 3. Cosa succede se non fissiamo il seme?

Se non impostiamo `random_state`, le parti casuali possono produrre risultati diversi a ogni esecuzione.

Per esempio:

```python
train_test_split(
    X,
    y,
    test_size=0.3
)
```

potrebbe dividere il dataset in modo diverso ogni volta.

Supponiamo di avere 10 righe:

```text
1  2  3  4  5  6  7  8  9  10
```

Prima esecuzione:

```text
Training: 1, 2, 4, 5, 7, 8, 10
Test:     3, 6, 9
```

Seconda esecuzione:

```text
Training: 1, 3, 4, 6, 7, 9, 10
Test:     2, 5, 8
```

Il programma è lo stesso, ma la suddivisione cambia.

---

# 4. Cosa succede invece con `random_state=42`?

Scrivendo:

```python
train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

la suddivisione viene resa riproducibile.

```text
Esecuzione 1
Training → stessi dati
Test     → stessi dati

Esecuzione 2
Training → stessi dati
Test     → stessi dati

Esecuzione 3
Training → stessi dati
Test     → stessi dati
```

Questo è molto utile durante un laboratorio.

Docente e partecipanti possono eseguire lo stesso codice e ottenere la stessa suddivisione dei dati.

---

# 5. Che cosa significa `test_size`?

Nel codice:

```python
train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

`test_size=0.3` significa:

```text
70% dei dati → TRAINING
30% dei dati → TEST
```

Con 100 osservazioni:

```text
100 osservazioni
      |
      +-- 70 → training
      |
      +-- 30 → test
```

Il **training set** serve per addestrare il modello.

```python
model.fit(X_train, y_train)
```

Il **test set** serve per verificare il modello su dati che non ha utilizzato per imparare.

```python
model.predict(X_test)
```

---

# 6. Perché separiamo training e test?

Il modello deve essere valutato su dati nuovi.

Se utilizzassimo gli stessi dati sia per imparare sia per valutare il modello:

```text
dati
 ↓
training
 ↓
valutazione sugli stessi dati
```

potremmo ottenere risultati troppo ottimistici.

Separando invece:

```text
Dataset
   |
   +-- Training set → il modello impara
   |
   +-- Test set     → verifichiamo il modello
```

possiamo capire meglio se il modello riesce a **generalizzare**.

---

# 7. Esempio completo

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

model = DecisionTreeClassifier(
    max_depth=2,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
```

In questo esempio ci sono due `random_state=42`.

Ma controllano due cose diverse.

---

# 8. Il primo `random_state=42`

Qui:

```python
train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

serve a rendere riproducibile la suddivisione del dataset.

```text
random_state=42
        ↓
stessa suddivisione
        ↓
stesso training set
        ↓
stesso test set
```

---

# 9. Il secondo `random_state=42`

Qui:

```python
DecisionTreeClassifier(
    max_depth=2,
    random_state=42
)
```

serve a controllare eventuali scelte pseudo-casuali interne all'algoritmo.

```text
random_state=42
        ↓
stesse scelte interne
        ↓
modello riproducibile
```

I due `42` hanno lo stesso valore, ma controllano due processi distinti.

Potremmo anche scrivere:

```python
train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=10
)

model = DecisionTreeClassifier(
    max_depth=2,
    random_state=25
)
```

Il codice sarebbe comunque riproducibile.

Non è necessario che i due valori siano uguali.

---

# 10. Perché senza seed possono cambiare anche le metriche?

Se cambia il modo in cui il dataset viene diviso:

```text
dataset
   ↓
training diverso
   ↓
modello appreso diverso
   ↓
test diverso
   ↓
prediction diverse
   ↓
metriche diverse
```

Per esempio, in una esecuzione potremmo ottenere:

```text
precision = 1.00
recall    = 0.78
```

e con una diversa suddivisione casuale:

```text
precision = 0.92
recall    = 0.82
```

Questo non significa necessariamente che il codice sia sbagliato.

Significa che abbiamo cambiato i dati usati per addestrare e valutare il modello.

Fissando il seed possiamo confrontare gli esperimenti nelle stesse condizioni.

---

# 11. Esempio intuitivo

Possiamo immaginare `random_state=42` come il comando:

> **"Ogni volta che devi fare una scelta casuale, parti sempre dallo stesso punto."**

Senza seed fisso:

```text
Esecuzione 1 → percorso casuale A
Esecuzione 2 → percorso casuale B
Esecuzione 3 → percorso casuale C
```

Con:

```python
random_state=42
```

otteniamo:

```text
Esecuzione 1 → percorso A
Esecuzione 2 → percorso A
Esecuzione 3 → percorso A
```

---

# 12. Concetti da ricordare

**`random_state=42`**

```text
fissa il seme
      ↓
controlla la casualità
      ↓
rende l'esperimento riproducibile
```

**`test_size=0.3`**

```text
70% training
30% test
```

**`fit()`**

```text
il modello impara
```

**`predict()`**

```text
il modello usa ciò che ha imparato
```

La frase da ricordare è:

> **Il valore 42 non rende il modello più intelligente o più accurato: serve semplicemente a poter ripetere lo stesso esperimento ottenendo le stesse scelte pseudo-casuali.**

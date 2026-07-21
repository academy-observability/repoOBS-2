# UD25 — Laboratorio guidato
# Python da zero sui dati del Catalogo prodotti — v6.1



Gli script contengono commenti nel formato:

```python
# MODIFICA GUIDATA - TASK X
```

Non è sufficiente eseguire i file senza aprirli nell'editor.

## Obiettivo

Eseguire, leggere e modificare nove script progressivi. L'ultimo script integra lettura CSV, conversioni, ciclo, condizione e contatori.

## Evidenza da preparare

Linux/WSL:

```bash
cp templates/evidence_ud25_template.md evidence/ud25_python_fundamentals.md
```

PowerShell:

```powershell
Copy-Item templates/evidence_ud25_template.md evidence/ud25_python_fundamentals.md
```

---

## Task 1 — Verificare Python e creare l'ambiente virtuale

### Ubuntu o WSL

Prima controllare il comando realmente disponibile:

```bash
python3 --version
```

Creare l'ambiente:

```bash
python3 -m venv .venv
```

Se compare un errore relativo a `venv` o `ensurepip`:

```bash
sudo apt update
sudo apt install -y python3-venv
python3 -m venv .venv
```

Attivare:

```bash
source .venv/bin/activate
```

Dopo l'attivazione verificare:

```bash
python --version
```

### Windows PowerShell

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

### Risultato atteso

Il prompt mostra normalmente `(.venv)` e il comando `python --version` indica Python 3.

### Significato

Su Ubuntu il comando globale può essere `python3`; dentro l'ambiente virtuale useremo `python` perché punta all'interprete isolato della UD.

---

## Task 2 — Primo script e prima modifica reale

### 1. Aprire il file

Nel pannello Explorer di VS Code aprire:

```text
src/01_first_script.py
```

### 2. Prima esecuzione

```bash
python src/01_first_script.py
```

Output iniziale atteso:

```text
Python è pronto per analizzare i dati osservabili.
Workload: Catalogo prodotti
```

### 3. Modifica

Cercare:

```python
# MODIFICA GUIDATA - TASK 2
```

Aggiungere sotto il commento:

```python
print("UD corrente: 25")
```

Salvare il file ed eseguire di nuovo.

### 4. Nuovo output atteso

Compare una terza riga:

```text
UD corrente: 25
```

---

## Task 3 — Variabili, tipi e un errore osservabile

Questo task non si limita a stampare un tipo: deve mostrare concretamente perché testo e numero non sono intercambiabili nei calcoli.

### 1. Aprire il file

```text
src/02_variables_and_types.py
```

Cercare:

```python
# MODIFICA GUIDATA - TASK 3
```

### 2. Prima esecuzione: valore numerico

Verificare che la riga sia:

```python
duration_ms = 125.4
```

Eseguire:

```bash
python src/02_variables_and_types.py
```

Output decisivo atteso:

```text
Tipo di duration_ms: <class 'float'>
Durata superiore a 120 ms: True
```

La variabile e la soglia sono entrambe numeriche, quindi il confronto `>` è valido.

### 3. Seconda esecuzione: trasformare il valore in testo

Sostituire **esattamente**:

```python
duration_ms = 125.4
```

con:

```python
duration_ms = "125.4"
```

Salvare ed eseguire di nuovo:

```bash
python src/02_variables_and_types.py
```

### 4. Risultato atteso

Le prime stampe funzionano, perché `print()` può visualizzare sia testo sia numeri. Il programma si interrompe però sulla riga:

```python
duration_ms > threshold_ms
```

con un errore simile a:

```text
TypeError: '>' not supported between instances of 'str' and 'float'
```

### 5. Perché accade

`print()` riceve un valore e ne costruisce una rappresentazione leggibile. Non deve decidere se `"125.4"` sia numericamente maggiore di `120.0`.

L'operatore `>` deve invece confrontare valori compatibili:

```text
float > float    valido
str   > float    non valido
```

### 6. Correzione

Sostituire la riga con:

```python
duration_ms = float("125.4")
```

Rieseguire. Il tipo torna `float` e il confronto produce nuovamente `True`.

### Domanda riformulata

Perché `print("125.4")` funziona, mentre `"125.4" > 120.0` genera un `TypeError`?

**Risposta attesa:** stampare significa rappresentare un valore; confrontare numericamente richiede due tipi numerici compatibili. La stringa deve prima essere convertita con `float()`.

---

## Task 4 — Condizioni `if`, `elif`, `else`

### File da aprire

```text
src/03_conditions.py
```

Cercare:

```python
# MODIFICA GUIDATA - TASK 4
```

Eseguire tre prove, salvando ed eseguendo dopo ogni modifica:

```python
status_code = 503
status_code = 404
status_code = 200
```

| Valore | Ramo atteso |
|---:|---|
| 503 | `if status_code >= 500` |
| 404 | `elif status_code >= 400` |
| 200 | `else` |

### Concetto

Le condizioni vengono valutate dall'alto verso il basso. Appena una condizione è vera, il relativo blocco viene eseguito e gli altri vengono saltati.

---

## Task 5 — Modificare una lista

### File da aprire

```text
src/04_lists.py
```

Prima eseguire lo script e annotare:

- numero di durate;
- durata massima.

Cercare:

```python
# MODIFICA GUIDATA - TASK 5
```

Togliere `#` dalla riga:

```python
# durations_ms.append(1500.0)
```

che deve diventare:

```python
durations_ms.append(1500.0)
```

Rieseguire.

### Cambiamenti attesi

- il numero passa da 4 a 5;
- il ciclo stampa `1500.0`;
- il massimo diventa `1500.0`.

---

## Task 6 — Aggiungere una coppia chiave/valore

### File da aprire

```text
src/05_dictionaries.py
```

Cercare le due sezioni `MODIFICA GUIDATA - TASK 6`.

### Parte A

Decommentare nel dizionario:

```python
"trace_id": "trace-example-001",
```

### Parte B

Decommentare:

```python
print("Trace ID:", request["trace_id"])
```

Salvare ed eseguire.

### Risultato atteso

Il dizionario e l'output contengono il nuovo `trace_id`.

### Controllo utile

Se si decommenta la `print` senza aggiungere prima la chiave, Python produce:

```text
KeyError: 'trace_id'
```

Questo dimostra che si può leggere soltanto una chiave presente nel dizionario.

---

## Task 7 — Filtrare una lista di dizionari

### File da aprire

```text
src/06_list_of_dictionaries.py
```

La prima esecuzione stampa tutte e tre le richieste.

### Modifica

Sostituire il ciclo finale:

```python
for request in requests:
    print(
        request["service"],
        request["endpoint"],
        request["status_code"],
        request["duration_ms"],
    )
```

con:

```python
for request in requests:
    if request["status_code"] >= 500:
        print(
            request["service"],
            request["endpoint"],
            request["status_code"],
            request["duration_ms"],
        )
```

### Attenzione all'indentazione

La `print()` appartiene al blocco `if` e deve essere rientrata di quattro spazi in più.

### Output atteso

Viene stampata soltanto la richiesta backend con status 500.

---

## Task 8 — Richiamare una funzione con parametri diversi

### File da aprire

```text
src/07_functions.py
```

Prima eseguire lo script. Poi cercare:

```python
# MODIFICA GUIDATA - TASK 8
```

Decommentare:

```python
print("Più lenta di 2000 ms:", is_slow(duration_ms, 2000.0))
```

### Output atteso

```text
Più lenta di 1000 ms: True
Più lenta di 2000 ms: False
```

La funzione è la stessa; cambia il valore del parametro `threshold_ms`.

---

## Task 9 — Aggiungere una colonna all'output CSV

### File da aprire

```text
src/08_read_csv_first_rows.py
```

Prima aprire anche:

```text
datasets/mini_products_requests.csv
```

Eseguire lo script e osservare le prime cinque righe.

Cercare:

```python
# MODIFICA GUIDATA - TASK 9
```

Decommentare:

```python
row["trace_id"],
```

Salvare ed eseguire di nuovo.

### Output atteso

Ogni riga stampata contiene anche il trace ID.

### Concetto

`row` è il dizionario della riga corrente; `trace_id` è una delle chiavi ricavate dall'intestazione CSV.

---

## Task 10 — Integrare i concetti senza una nuova modifica

### File

```text
src/09_count_errors.py
```

Questo task è volutamente di lettura e spiegazione. Non deve essere contato tra le modifiche richieste.

Prima dell'esecuzione prevedere:

- quante righe contiene il dataset;
- quante hanno status 500 o superiore.

Eseguire:

```bash
python src/09_count_errors.py
```

Poi spiegare il flusso usando questa sequenza:

```text
open → DictReader → for row → int(status_code) → if → contatore → print finale
```

Lo script conta un segnale tecnico; non stabilisce se esiste un incidente.

---

## Task 11 — Controllo finale

Nel file evidence riportare almeno:

1. una modifica effettuata e il relativo output prima/dopo;
2. il `TypeError` del Task 3 e la sua correzione;
3. il significato di lista e dizionario;
4. il ruolo di `for` e `if`;
5. il motivo delle conversioni `int()` e `float()`;
6. la spiegazione del flusso dello script 09.

## Criterio di completamento

Il laboratorio è completato quando:

- gli script sono stati aperti e letti;
- almeno sette modifiche guidate sono state eseguite;
- il Task 3 ha mostrato e corretto il `TypeError`;
- l'evidenza descrive il significato dei risultati, non soltanto i comandi eseguiti.

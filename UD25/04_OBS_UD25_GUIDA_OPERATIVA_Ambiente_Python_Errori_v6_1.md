# UD25 — Guida operativa
# Ambiente Python, esecuzione e primi errori

## 1. Aprire la cartella corretta

In VS Code apriamo la cartella `UD25`, non un singolo file. Nel terminale verifichiamo:

```bash
pwd
```

In PowerShell:

```powershell
Get-Location
```

Dobbiamo vedere il percorso che termina con `UD25`.

## 2. Verificare Python nel proprio sistema

### Ubuntu e WSL

Usare prima:

```bash
python3 --version
```

Il messaggio `Command 'python' not found` non dimostra che Python 3 sia assente: su Ubuntu il comando globale è spesso `python3`.

### Windows PowerShell

Provare:

```powershell
py -3 --version
```

In alternativa, se configurato:

```powershell
python --version
```

## 3. Creare l'ambiente virtuale

L'ambiente virtuale isola l'interprete e le eventuali dipendenze del progetto.

### Ubuntu e WSL

```bash
python3 -m venv .venv
```

Se compare un errore relativo a `venv` o `ensurepip`:

```bash
sudo apt update
sudo apt install -y python3-venv
python3 -m venv .venv
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
```

### Attivazione PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Attivazione WSL/Linux

```bash
source .venv/bin/activate
```

Quando è attivo, il prompt mostra normalmente `(.venv)`.

In UD25 non installiamo pacchetti: `csv` e `pathlib` sono nella libreria standard.

## 4. Eseguire uno script

```bash
python src/01_first_script.py
```

Risultato atteso:

```text
Python è pronto per analizzare i dati osservabili.
Workload: Catalogo prodotti
```

## 5. Errori comuni

### `Command 'python' not found` su Ubuntu/WSL

Verificare con:

```bash
python3 --version
```

Creare l'ambiente con `python3 -m venv .venv`, attivarlo e usare poi `python` dentro `.venv`. Non è necessario installare globalmente `python-is-python3`.

### `can't open file`

Il percorso dello script non è corretto. Controllare la directory corrente e il nome del file.

### `SyntaxError`

Python non riesce a interpretare il codice. Controllare parentesi, virgolette e due punti.

### `IndentationError`

Il blocco dopo `if`, `for` o `def` non è rientrato correttamente.

### `TypeError: '>=' not supported between instances of 'str' and 'int'`

Si sta confrontando testo con numero. Convertire:

```python
status_code = int(row["status_code"])
```

### `KeyError: 'nome_colonna'`

La chiave richiesta non coincide con un'intestazione del CSV. Controllare maiuscole, minuscole e underscore.

### `FileNotFoundError`

Il dataset non è nel percorso previsto. Verificare:

```text
datasets/mini_products_requests.csv
```

## 6. Come leggere un traceback

Il traceback va letto dal basso verso l'alto:

1. ultima riga: tipo e messaggio dell'errore;
2. riga precedente: file e numero di riga;
3. risalire solo se serve capire la catena delle chiamate.

Non correggiamo casualmente il codice: individuiamo prima il punto e il tipo dell'errore.

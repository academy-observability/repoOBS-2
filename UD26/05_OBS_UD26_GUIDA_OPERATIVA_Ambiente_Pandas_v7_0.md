# UD26 — Guida operativa
# Preparare Python e pandas

## 1. Entrare nella cartella UD26

Linux / WSL:

```bash
cd UD26
```

Verificare Python:

```bash
python3 --version
```

Su Ubuntu/WSL il comando disponibile può essere `python3` invece di `python`.

---

## 2. Creare l'ambiente virtuale

```bash
python3 -m venv .venv
```

Se Ubuntu segnala che `venv` non è disponibile:

```bash
sudo apt update
sudo apt install -y python3-venv
```

Poi ripetere:

```bash
python3 -m venv .venv
```

Attivazione Linux / WSL:

```bash
source .venv/bin/activate
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Dopo l'attivazione verificare:

```bash
python --version
```

---

## 3. Installare pandas

```bash
python -m pip install -r requirements.txt
```

Verificare:

```bash
python -c "import pandas; print(pandas.__version__)"
```

---

## 4. Dove si trova il dataset

```text
UD26/
├── datasets/
│   └── mini_products_requests.csv
└── src/
```

Usiamo lo stesso mini dataset già conosciuto, così il nuovo elemento della giornata è il DataFrame, non un nuovo scenario.

---

## 5. Eseguire gli script

Dalla radice `UD26`:

```bash
python src/01_load_dataframe.py
```

Poi, nell'ordine:

```bash
python src/02_select_column.py
python src/03_filter_service.py
python src/04_filter_server_errors.py
```

---

## 6. Errore: `No module named pandas`

Controllare che l'ambiente virtuale sia attivo:

```bash
python -c "import sys; print(sys.executable)"
```

Poi:

```bash
python -m pip show pandas
```

Se non compare alcun pacchetto:

```bash
python -m pip install -r requirements.txt
```

---

## 7. Regola importante

Gli script leggono il CSV, ma non lo sovrascrivono.

Le modifiche guidate riguardano il codice Python e i sottoinsiemi creati in memoria.

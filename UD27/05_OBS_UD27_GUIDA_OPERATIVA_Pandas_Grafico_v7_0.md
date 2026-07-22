# UD27 — Guida operativa
# Ambiente pandas e grafico semplice

## 1. Creare l'ambiente virtuale

Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Installare le dipendenze

```bash
python -m pip install -r requirements.txt
```

Verifica:

```bash
python -c "import pandas, matplotlib; print('pandas', pandas.__version__); print('matplotlib', matplotlib.__version__)"
```

## 3. Che cosa dobbiamo comprendere

In questa UD il codice centrale riguarda:

- selezione delle durate;
- statistiche;
- filtri;
- `groupby`;
- p95.

La configurazione tecnica del grafico è **codice di servizio**.

Non è richiesto imparare l'intera libreria matplotlib.

## 4. Eseguire gli script

Dalla cartella `UD27`:

```bash
python src/01_basic_statistics.py
python src/02_statistics_one_group.py
python src/03_group_data.py
python src/04_calculate_p95.py
python src/05_plot_one_group.py
```

## 5. Output del grafico

Lo script 05 crea:

```text
outputs/frontend_products_duration.png
```

Non è necessario che si apra automaticamente una finestra grafica.

Aprire il file PNG con l'editor o il visualizzatore disponibile.

## 6. Troubleshooting essenziale

### `ModuleNotFoundError`

Verificare che l'ambiente virtuale sia attivo e reinstallare:

```bash
python -m pip install -r requirements.txt
```

### File CSV non trovato

Verificare la struttura:

```text
UD27/
├── datasets/
│   └── mini_products_requests.csv
└── src/
```

### Grafico non creato

Controllare:

```text
outputs/
```

e verificare che matplotlib sia installato.

## 7. Regola della giornata

Non modificare il CSV originale.

Le modifiche richieste riguardano gli script e i filtri in memoria.

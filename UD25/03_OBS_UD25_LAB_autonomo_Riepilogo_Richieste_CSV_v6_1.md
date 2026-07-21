# UD25 — Laboratorio autonomo
# Riepilogo elementare delle richieste CSV

## Scenario

Il team ha ricevuto un piccolo estratto delle osservazioni del Catalogo prodotti. Serve un riepilogo ripetibile che non dipenda dal conteggio manuale.

## Obiettivo

Completare uno script che:

1. legge `datasets/mini_products_requests.csv`;
2. conta tutte le righe;
3. conta gli status 5xx;
4. individua la riga con durata massima;
5. salva servizio, endpoint e request ID della riga più lenta;
6. scrive il risultato in `outputs/basic_request_summary.txt`.

## Preparazione

Creare la cartella di lavoro e copiare lo starter:

```bash
mkdir -p src/partecipante
cp src/starter/summarize_requests_basic_TODO.py src/partecipante/summarize_requests_basic.py
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force src/partecipante
Copy-Item src/starter/summarize_requests_basic_TODO.py src/partecipante/summarize_requests_basic.py
```

## Vincoli

- non usare pandas;
- non modificare il CSV;
- convertire `status_code` e `duration_ms`;
- non scrivere a mano i risultati;
- mantenere il percorso di input relativo;
- sostituire tutti i `TODO` e rimuovere `pass`.

## Metodo consigliato

Prima di programmare, annotare le variabili necessarie:

```text
total_rows
server_errors
slowest_duration_ms
slowest_service
slowest_endpoint
slowest_request_id
```

Poi completare un blocco alla volta.

## Esecuzione

```bash
python src/partecipante/summarize_requests_basic.py
```

## Verifiche

```bash
cat outputs/basic_request_summary.txt
```

PowerShell:

```powershell
Get-Content outputs/basic_request_summary.txt
```

Il file deve contenere:

- totale righe;
- totale righe 5xx;
- durata massima;
- servizio, endpoint e request ID della riga più lenta.

## Troubleshooting

### La durata massima resta `-1`

La variabile non viene aggiornata oppure `duration_ms` non è stata convertita.

### Il contatore 5xx resta zero

Controllare il confronto e il tipo di `status_code`.

### L'output contiene `DA COMPLETARE`

Il testo finale non è stato sostituito.

## Evidenze da consegnare

```text
src/partecipante/summarize_requests_basic.py
outputs/basic_request_summary.txt
evidence/ud25_python_fundamentals.md
```

## Criteri di accettazione

- script eseguibile senza modifiche manuali ai percorsi;
- risultati derivati dal CSV;
- codice leggibile e commentato nei passaggi decisivi;
- spiegazione orale o scritta del ciclo, delle conversioni e dell'aggiornamento del massimo.

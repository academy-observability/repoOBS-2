Da: Andrea Bello
- Per il punto 9 del Guidato UD04, consiglio di installare da riga di comando la libreria jq 
(documentazione reperibile qui: https://jqlang.org/).
- Per installarla da riga di comando basta fare: sudo apt install jq.
- Poi nel comando tail "-n ... | " sostituite "python3 -m json.tool" con "jq ."

## Spiegazione
###  Nota su formattazione dei log JSON con `jq`

Durante la UD04 lavoriamo con il file:

```text
logs/app.log
````

Il file contiene log in formato JSON Lines: ogni riga è un oggetto JSON autonomo.

Esempio:

```json
{"ts":"2026-06-24T10:20:30Z","level":"INFO","request_id":"test-001","path":"/health","status":200,"duration_ms":4}
```

Per leggere meglio una singola riga possiamo usare:

```bash
tail -n 1 logs/app.log | python3 -m json.tool
```

Se però vogliamo formattare più righe, ad esempio:

```bash
tail -n 3 logs/app.log
```

è preferibile usare `jq`, uno strumento da riga di comando per leggere e formattare JSON.

### Installazione di `jq`

Su Ubuntu/WSL:

```bash
sudo apt update
sudo apt install -y jq
```

Verifica:

```bash
jq --version
```

### Uso consigliato

Per formattare le ultime 3 righe del log:

```bash
tail -n 3 logs/app.log | jq .
```

Questo comando legge ogni riga JSON e la stampa in modo leggibile.

### Alternativa senza `jq`

Se `jq` non è disponibile, usare `python3 -m json.tool` su una sola riga:

```bash
tail -n 1 logs/app.log | python3 -m json.tool
```

Oppure, per più righe:

```bash
tail -n 3 logs/app.log | while read line; do echo "$line" | python3 -m json.tool; done
```

Nota: il comando seguente può generare errore se il file contiene più oggetti JSON separati su righe diverse:

```bash
tail -n 3 logs/app.log | python3 -m json.tool
```

```
```


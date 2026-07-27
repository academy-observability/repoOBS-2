# LAB guidato — Ollama da Python e telemetria essenziale

## Durata

105 minuti.

## Obiettivo

Passare dalla chat interattiva a chiamate programmabili e osservabili.

## 1. Preparazione

```bash
source .venv/bin/activate
export OLLAMA_MODEL="llama3.2:1b"
```

Mirrored:

```bash
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
```

NAT:

```bash
export WINDOWS_HOST=$(ip route show | awk '/default/ {print $3; exit}')
export OLLAMA_BASE_URL="http://$WINDOWS_HOST:11434"
```

## 2. Controllo

```bash
python3 scripts/00_check_ollama.py
```

## 3. Prima chiamata Python

```bash
python3 scripts/01_first_chat.py
```

Osservare:

- endpoint;
- modello;
- testo;
- durata client;
- token di input e output.

## 4. Confronto tra prompt

```bash
python3 scripts/02_compare_prompts.py
```

Lo script usa lo stesso evidence packet con prompt aperto e vincolato e salva i risultati in `outputs/`.

Domande:

1. Quale risposta è più strutturata?
2. Quale cita meglio le evidenze?
3. Il prompt vincolato elimina tutti i claim non supportati?

## 5. Raccolta telemetria

```bash
python3 scripts/03_collect_telemetry.py
```

Output:

```text
outputs/ollama_telemetry.csv
```

Aprire:

```bash
column -s, -t < outputs/ollama_telemetry.csv | less -S
```

## 6. Analisi offline

```bash
python3 scripts/04_analyze_telemetry.py
```

Se non è stato possibile produrre dati reali:

```bash
python3 scripts/04_analyze_telemetry.py fallback/telemetry/ollama_telemetry_fallback.csv
```

## 7. Confronto modelli opzionale

Solo se entrambi sono già scaricati:

```bash
export OLLAMA_MODELS="llama3.2:1b,gemma3:1b"
python3 scripts/05_compare_models.py
```

Non scaricare modelli aggiuntivi durante la fase centrale della lezione.

## 8. Interpretazione

Rispondere nel file `outputs/interpretazione_telemetria.md`:

1. La prima chiamata ha una `load_duration` maggiore?
2. Qual è la mediana della durata client?
3. Quanti token di output sono stati prodotti?
4. Il minor numero di token indica automaticamente una risposta migliore?
5. Quale metrica tecnica non misura la correttezza semantica?

## Risultato atteso

Il partecipante sa distinguere:

```text
funzionamento tecnico
prestazioni
consumo token
qualità/verificabilità
```

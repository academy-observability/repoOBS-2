# Script UD30

## Ordine di esecuzione

```text
00_check_ollama.py
01_first_chat.py
02_compare_prompts.py
03_collect_telemetry.py
04_analyze_telemetry.py
05_compare_models.py
```

## Codice da comprendere

- import del client Ollama;
- scelta del modello;
- costruzione del messaggio;
- chiamata `client.chat()`;
- lettura di `message.content`;
- campi di token e durata;
- registrazione CSV;
- analisi pandas.

## Codice di servizio

`common.py` contiene:

- risoluzione percorsi;
- conversione nanosecondi → millisecondi;
- normalizzazione di oggetti e dizionari;
- gestione uniforme degli errori.

Queste funzioni sono commentate, ma non rappresentano il salto concettuale principale della UD.

# UD30 — Observability for AI: esito, durate e token

## 1. Perché osservare l'inferenza

Quando l'LLM entra nel flusso applicativo, può fallire in modi diversi:

- errore di connessione;
- modello non disponibile;
- timeout;
- risposta vuota;
- latenza elevata;
- consumo elevato di token;
- testo tecnicamente riuscito ma semanticamente debole.

Un HTTP 200 o una chiamata completata non dimostrano che la risposta sia utile.

## 2. Misure minime della UD

| Campo | Significato |
|---|---|
| `success` | chiamata completata senza errore tecnico |
| `client_duration_ms` | tempo misurato dallo script |
| `total_duration_ms` | durata totale riportata da Ollama |
| `load_duration_ms` | caricamento del modello |
| `prompt_eval_count` | token di input elaborati |
| `eval_count` | token di output generati |
| `prompt_eval_duration_ms` | tempo per elaborare il prompt |
| `eval_duration_ms` | tempo per generare l'output |

## 3. Perché client e server possono differire

```text
client_duration
=
rete locale + accodamento + elaborazione + serializzazione + ritorno
```

`total_duration` è la misura esposta dal runtime. Le due misure non devono essere forzatamente identiche.

## 4. Prima richiesta e caricamento

La prima richiesta può essere più lenta perché il modello viene caricato in memoria.

```text
prima richiesta: load_duration elevata
richieste successive: modello già residente
```

## 5. Throughput dei token

Una stima semplice:

```text
token al secondo = eval_count / eval_duration_seconds
```

Il valore aiuta a confrontare esecuzioni sullo stesso ambiente, ma non misura la qualità della risposta.

## 6. Telemetria e qualità

Queste due dimensioni sono complementari:

```text
telemetria tecnica
→ il sistema ha risposto? quanto ha impiegato? quanti token?

valutazione semantica
→ i claim sono supportati? la risposta segue i vincoli?
```

Un modello può essere veloce e sbagliare. Può essere lento e produrre una risposta valida. La decisione richiede entrambe le viste.

## 7. Limiti

Il laboratorio non introduce una piattaforma APM per LLM. Usa CSV e pandas per rendere osservabili pochi segnali essenziali, mantenendo un solo salto concettuale.

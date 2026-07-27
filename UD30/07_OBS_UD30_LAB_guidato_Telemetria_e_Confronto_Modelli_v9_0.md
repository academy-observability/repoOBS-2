# LAB guidato — Telemetria delle chiamate e confronto tra modelli

## Durata indicativa

90 minuti.

## Obiettivo

Registrare telemetria reale delle chiamate Ollama e collegarla a una valutazione manuale del contenuto.

Non implementeremo dashboard, tracing distribuito o un servizio web. Useremo un CSV per rendere osservabili le chiamate effettuate dallo script.

---

## Task 1 — Leggere lo script di raccolta

Aprire:

```text
scripts/03_collect_telemetry.py
```

Lo script esegue più chiamate e registra:

```text
timestamp
run_id
model
prompt_type
status
client_latency_ms
ollama_total_ms
load_ms
prompt_eval_ms
generation_ms
prompt_tokens
output_tokens
response_length
error
```

### Significato

- `client_latency_ms`: tempo osservato dall’applicazione Python;
- `ollama_total_ms`: durata complessiva riportata da Ollama;
- `load_ms`: tempo per rendere disponibile il modello;
- `prompt_eval_ms`: elaborazione del prompt;
- `generation_ms`: generazione dei token;
- `status`: esito tecnico.

---

## Task 2 — Raccogliere tre esecuzioni

Impostare il modello:

```bash
export OLLAMA_MODEL=llama3.2:1b
```

Eseguire:

```bash
python3 scripts/03_collect_telemetry.py --runs 3
```

Il CSV viene scritto in:

```text
runtime/ollama_runs.csv
```

Lo script registra sia il prompt aperto sia quello vincolato per ogni ciclo.

### Domande

- La prima chiamata mostra `load_ms` maggiore?
- La latenza è identica in tutte le esecuzioni?
- Il prompt vincolato usa più token?
- La risposta più lunga coincide sempre con la chiamata più lenta?

---

## Task 3 — Analizzare con pandas

```bash
python3 scripts/04_analyze_telemetry.py
```

Lo script stampa:

- numero di chiamate;
- successi ed errori;
- latenza media e p95;
- token medi per tipo di prompt;
- confronto per modello;
- chiamata più lenta.

### Collegamento con UD27

Le operazioni `groupby`, `mean`, `quantile` e `value_counts` sono già note. La novità non è pandas: è comprendere che stiamo osservando una dipendenza AI reale.

---

## Task 4 — Aggiungere la valutazione qualitativa

Aprire i file delle risposte prodotti dallo script e assegnare manualmente:

```text
quality_status = supported | partially_supported | unsupported
```

Usare almeno questi criteri:

- separazione fatti/ipotesi;
- presenza di claim inventati;
- rispetto della struttura;
- utilità delle verifiche.

Compilare `templates/valutazione_risposte.csv` oppure una copia.

### Perché è manuale

Un controllo automatico della qualità richiederebbe un nuovo metodo di valutazione, nuovi dati di riferimento e ulteriori assunzioni. In questa UD vogliamo rendere visibile la differenza tra metrica tecnica e giudizio sul contenuto.

---

## Task 5 — Confrontare due modelli

Se il PC lo consente:

```bash
export OLLAMA_MODELS=llama3.2:1b,llama3.2:3b
python3 scripts/05_compare_models.py
```

Su PC limitati:

```bash
export OLLAMA_MODELS=gemma3:1b,llama3.2:1b
python3 scripts/05_compare_models.py
```

Se non è possibile eseguire due modelli, usare:

```text
datasets/fallback_model_comparison.csv
```

---

## Task 6 — Compilare la matrice di confronto

| Dimensione | Modello A | Modello B |
|---|---:|---:|
| Dimensione indicativa del pacchetto | | |
| Latenza client | | |
| Token output | | |
| Rispetto struttura | | |
| Claim non supportati | | |
| Verifiche utili | | |
| Eseguibilità sul PC | | |

### Domande

1. Il modello più grande è più lento?
2. Segue meglio il prompt?
3. Produce meno claim non supportati?
4. La differenza è sufficiente a giustificare più risorse?
5. Quale modello sceglieresti per questo specifico compito?

Non generalizzare la risposta a tutti i possibili usi degli LLM.

---

## Task 7 — Individuare l’errore semantico

Cercare una riga con:

```text
status = success
```

ma con valutazione:

```text
quality_status = unsupported
```

Spiegare in una frase:

- perché la chiamata è tecnicamente riuscita;
- perché il risultato è comunque inutilizzabile.

Questa è la distinzione fondamentale di Observability for AI.

---

## Task 8 — Proporre quattro pannelli, senza implementarli

Progettare una dashboard concettuale con soli quattro pannelli:

1. chiamate e failure tecniche;
2. latenza p50/p95 per modello;
3. token input/output per modello;
4. distribuzione della valutazione qualitativa.

Per ciascun pannello indicare:

- dato necessario;
- domanda a cui risponde;
- limite interpretativo.

Esempio:

```text
Pannello: latenza p95
Domanda: quale modello degrada l’esperienza?
Limite: non indica se la risposta è corretta.
```

---

## Conclusione

```text
telemetria tecnica
→ descrive esecuzione e consumo

valutazione qualitativa
→ descrive adeguatezza del contenuto
```

Nessuna delle due dimensioni è sufficiente da sola.

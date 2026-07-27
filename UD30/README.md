# UD30 — AI generativa a supporto dell’analisi degli incidenti

## Versione 9.0

Questa unità conclude il percorso Academy Observability collegando le competenze già acquisite su dati, statistiche, anomaly detection, Machine Learning spiegabile, log, metriche e trace all’uso controllato di un Large Language Model.

La UD dura **8 ore** ed è organizzata in due mezze giornate:

- **prima parte:** comprendere LLM, assistenti cloud, Ollama e modelli locali;
- **seconda parte:** usare un LLM nell’analisi di un incidente e osservare tecnicamente le chiamate effettuate da Python.

## Obiettivo principale

> Usare un LLM come assistente dell’analisi senza confondere una risposta plausibile con un’evidenza tecnica.

## Progressione

```text
UD28: regole statistiche → anomalia
UD29: feature → Decision Tree → classificazione
UD30: evidenze → LLM → testo e ipotesi da verificare
```

## File teorici

1. `00_OBS_UD30_Dal_Machine_Learning_agli_LLM_v9_0.md`
2. `01_OBS_UD30_Assistenti_Cloud_Ollama_e_Modelli_Locali_v9_0.md`
3. `02_OBS_UD30_Modelli_Ollama_Tag_Dimensioni_Quantizzazione_v9_0.md`
4. `03_OBS_UD30_AI_Assisted_Observability_e_Observability_For_AI_v9_0.md`

## Laboratori

1. `04_OBS_UD30_LAB_guidato_Confronto_Cloud_e_Ollama_Chat_v9_0.md`
2. `05_OBS_UD30_LAB_guidato_Ollama_da_Python_v9_0.md`
3. `06_OBS_UD30_LAB_guidato_Analisi_Incidente_con_LLM_v9_0.md`
4. `07_OBS_UD30_LAB_guidato_Telemetria_e_Confronto_Modelli_v9_0.md`
5. `08_OBS_UD30_LAB_autonomo_Handoff_AI_Verificabile_v9_0.md`

## Modelli previsti

- riferimento: `llama3.2:1b`;
- confronto, quando il PC lo consente: `llama3.2:3b`;
- fallback leggero: `gemma3:1b`;
- fallback estremo, solo per integrazione e telemetria: `gemma3:270m`;
- continuità didattica: risposte e CSV già predisposti nella cartella `fallback`.

I nomi dei modelli sono configurabili tramite la variabile d’ambiente `OLLAMA_MODEL`. Gli script non richiedono modifiche al codice per cambiare modello.

## Prerequisiti

- Python 3.10 o successivo;
- Ollama installato e in esecuzione;
- almeno un modello locale scaricato;
- package Python `ollama` e `pandas`.

Consultare prima della lezione:

- `09_OBS_UD30_Guida_Operativa_Preparazione_Ambiente_v9_0.md`;
- `09A_OBS_UD30_Preflight_Compatibilita_e_Prima_Chat_Ollama_WSL_v9_0.md`.

# UD30 — AI-assisted Observability con LLM cloud e Ollama locale

## Scopo

Questa unità conclude il percorso passando da modelli che producono risultati strutturati a modelli generativi che producono testo, sintesi e ipotesi.

Il salto concettuale centrale è:

```text
UD29
feature → Decision Tree → classe

UD30
evidenze + istruzione → LLM → testo da verificare
```

L'LLM non sostituisce metriche, log, trace o valutazione tecnica. Riceve un **evidence packet** e aiuta a:

- riassumere fatti osservati;
- separare fatti e ipotesi;
- proporre verifiche;
- preparare un handoff leggibile;
- osservare token, tempi ed esito dell'inferenza locale.

## Architettura operativa ufficiale

Ollama viene installato ed eseguito in **Windows**. I file, gli script Python e i comandi del laboratorio vengono eseguiti in **WSL Ubuntu**.

```text
Windows
├── Ollama
├── API locale 11434
└── modelli scaricati

WSL Ubuntu
├── terminale
├── Python + .venv
├── package ollama
└── script UD30 → API Ollama Windows
```

Non installare una seconda istanza di Ollama dentro WSL.

## Sequenza consigliata

1. `00_OBS_UD30_Dal_Machine_Learning_agli_LLM_v10_0.md`
2. `00A_OBS_UD30_Setup_Ollama_Windows_e_API_da_WSL_v10_0.md`
3. `00B_OBS_UD30_Preflight_Ollama_Windows_Client_WSL_v10_0.md`
4. `01_OBS_UD30_Assistenti_Cloud_Ollama_e_Modelli_Locali_v10_0.md`
5. `02_OBS_UD30_Evidence_Packet_Prompt_e_Verificabilita_v10_0.md`
6. `03_OBS_UD30_Observability_for_AI_Token_Durate_Esito_v10_0.md`
7. `04_OBS_UD30_LAB_guidato_Confronto_Cloud_e_Ollama_Chat_v10_0.md`
8. `05_OBS_UD30_LAB_guidato_Ollama_da_Python_e_Telemetria_v10_0.md`
9. `06_OBS_UD30_MINI_ATTIVITA_Fatti_Ipotesi_Verifiche_v10_0.md`
10. `07_OBS_UD30_LAB_autonomo_Handoff_Incidente_con_LLM_v10_0.md`
11. `08_OBS_UD30_Raccordo_Finale_AI_Assisted_Observability_v10_0.md`

## Durata indicativa

| Fase | Durata |
|---|---:|
| Apertura e concetti | 75 min |
| Setup/preflight | 45 min |
| Confronto cloud/Ollama Chat | 90 min |
| Python e telemetria | 105 min |
| Mini-attività e review | 45 min |
| Laboratorio autonomo | 90 min |
| Chiusura | 30 min |
| **Totale** | **8 ore** |

## Modelli

Modello di riferimento:

```text
llama3.2:1b
```

Fallback qualitativo:

```text
gemma3:1b
```

Fallback estremo, soltanto per verificare la catena tecnica:

```text
gemma3:270m
```

Usare sempre il tag esplicito. Non sostituire automaticamente il tag con `latest` o con un nome generico.

## Preparazione Python

Da WSL, nella cartella `UD30`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

## Variabili principali

Percorso mirrored:

```bash
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
export OLLAMA_MODEL="llama3.2:1b"
```

Percorso NAT:

```bash
export WINDOWS_HOST=$(ip route show | awk '/default/ {print $3; exit}')
export OLLAMA_BASE_URL="http://$WINDOWS_HOST:11434"
export OLLAMA_MODEL="llama3.2:1b"
```

La configurazione di rete va completata seguendo il file `00A`.

## Output attesi

- scheda di confronto cloud/locale;
- risposte a prompt aperto e vincolato;
- CSV con telemetria locale;
- analisi pandas dei tempi e dei token;
- matrice claim–evidence;
- handoff tecnico dell'incidente autonomo;
- evidenza dell'ambiente effettivamente usato.

## Regola di sicurezza

Utilizzare soltanto dati sintetici forniti nella UD. Non inserire in servizi cloud credenziali, segreti, dati personali, log reali o informazioni aziendali non autorizzate.

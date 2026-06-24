# OBS_UD04 – Laboratorio guidato: primo servizio osservabile

## Obiettivo del laboratorio

In questo laboratorio costruiamo ed eseguiamo un piccolo servizio HTTP locale progettato per essere osservabile. Il servizio espone endpoint di verifica, produce log JSON, restituisce un `X-Request-Id`, espone metriche minime e permette di calcolare SLI a partire dai log.

Lavoriamo in modo progressivo:

```text
servizio HTTP → log JSON → request-id → metriche → parser SLI → report
```

## 1. Preparazione cartelle

Posizioniamoci nella cartella della UD04.

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD04_Primo_Servizio_Osservabile
pwd
ls -la
```

Verifichiamo la struttura:

```bash
find . -maxdepth 2 -type f | sort
```

Dovremmo vedere almeno:

```text
src/observable_service.py
src/generate_traffic.sh
src/parse_sli.py
src/verifica_ud04.sh
config/service.env.example
```

## 2. Controllo prerequisiti

```bash
python3 --version
which python3 curl grep tail wc
```

Rendiamo eseguibili gli script Bash:

```bash
chmod 755 src/generate_traffic.sh src/verifica_ud04.sh
```

## 3. Lettura iniziale del servizio

Apriamo il file:

```bash
less src/observable_service.py
```

Individuiamo le parti principali:

| Sezione | Funzione |
|---|---|
| variabili `PORT`, `LOG_PATH`, `SERVICE_NAME`, `SERVICE_VERSION` | configurazione tramite ambiente |
| funzione `write_log` | scrittura log JSON |
| classe `MetricsStore` | raccolta metriche in memoria |
| classe `Handler` | gestione richieste HTTP |
| endpoint `/health` | verifica processo vivo |
| endpoint `/ready` | verifica servizio pronto |
| endpoint `/metrics` | metriche minime |
| endpoint `/work` | simulazione lavoro e latenza |
| endpoint `/fail` | errore controllato |

## 4. Avvio del servizio

Creiamo le cartelle runtime:

```bash
mkdir -p logs evidence docs
```

Avviamo il servizio sulla porta 9100:

```bash
PORT=9100 LOG_PATH="logs/app.log" python3 src/observable_service.py
```

Il terminale resta occupato. Lasciamolo aperto.

Apriamo un secondo terminale nella stessa cartella.

## 5. Verifica degli endpoint principali

Nel secondo terminale:

```bash
curl -i http://localhost:9100/health
```

Osserviamo:

- status HTTP `200`;
- header `Content-Type`;
- header `X-Request-Id`;
- body JSON.

Verifichiamo readiness:

```bash
curl -i http://localhost:9100/ready
```

Verifichiamo il tempo corrente:

```bash
curl -s http://localhost:9100/time
```

Verifichiamo le metriche:

```bash
curl -s http://localhost:9100/metrics
```

Dopo alcune richieste, le metriche devono iniziare a cambiare.

## 6. Correlazione con request-id esplicito

Inviamo una richiesta con request-id scelto da noi:

```bash
curl -i -H 'X-Request-Id: ud04-guidato-001' http://localhost:9100/health
```

Cerchiamo la riga di log corrispondente:

```bash
grep 'ud04-guidato-001' logs/app.log
```

Osserviamo che lo stesso identificativo è presente sia nella risposta HTTP sia nel file di log.

Questa è una prima forma di correlazione.

## 7. Osservazione del file di log

Visualizziamo le ultime righe:

```bash
tail -n 5 logs/app.log
```

Formattiamo una riga JSON con Python:

```bash
tail -n 1 logs/app.log | python3 -m json.tool
```

I campi principali sono:

| Campo | Significato |
|---|---|
| `ts` | timestamp evento |
| `level` | livello log |
| `request_id` | identificatore richiesta |
| `method` | metodo HTTP |
| `path` | endpoint richiesto |
| `status` | status HTTP restituito |
| `duration_ms` | durata della richiesta |
| `service` | nome del servizio |
| `version` | versione del servizio |

## 8. Generazione traffico controllato

Eseguiamo lo script di traffico:

```bash
src/generate_traffic.sh 9100 40
```

Lo script chiama endpoint riusciti, endpoint lenti ed endpoint con errore controllato.

Verifichiamo il numero di righe di log:

```bash
wc -l logs/app.log
```

Verifichiamo la presenza di errori:

```bash
grep '"status": 500' logs/app.log | head
grep '"status": 404' logs/app.log | head
grep '"status": 400' logs/app.log | head
```

## 9. Endpoint lento controllato

Usiamo `/work` per simulare una richiesta con durata specifica.

```bash
curl -i 'http://localhost:9100/work?ms=300'
```

Cerchiamo nel log:

```bash
tail -n 3 logs/app.log | python3 -m json.tool
```

La durata registrata deve essere coerente con il ritardo richiesto.

## 10. Readiness non disponibile

Interrompiamo il servizio con `CTRL+C`.

Riavviamolo simulando un servizio non pronto:

```bash
PORT=9100 READY=false LOG_PATH="logs/app.log" python3 src/observable_service.py
```

Da un secondo terminale:

```bash
curl -i http://localhost:9100/ready
```

Dovremmo ottenere `503 Service Unavailable`.

Fermiamo di nuovo il servizio e riavviamolo in modalità normale:

```bash
PORT=9100 READY=true LOG_PATH="logs/app.log" python3 src/observable_service.py
```

## 11. Calcolo SLI dai log

Eseguiamo il parser:

```bash
python3 src/parse_sli.py logs/app.log evidence/sli_report.json
```

Visualizziamo il report:

```bash
cat evidence/sli_report.json | python3 -m json.tool
```

Il report deve contenere almeno:

- `total_requests`;
- `error_rate_percent`;
- `availability_percent`;
- `latency_p50_ms`;
- `latency_p95_ms`;
- `status_breakdown`;
- `top_paths`;
- `sample_request_ids`.

## 12. Interpretazione minima degli indicatori

Leggiamo i valori ottenuti.

Esempio di interpretazione:

| Indicatore | Domanda |
|---|---|
| `total_requests` | quanto traffico è stato generato? |
| `error_rate_percent` | quante richieste sono fallite? |
| `availability_percent` | quante richieste hanno avuto esito positivo? |
| `latency_p95_ms` | quanto sono lente le richieste peggiori frequenti? |
| `top_paths` | quali endpoint vengono usati di più? |

## 13. Report tecnico

Creiamo il file:

```bash
nano docs/report_ud04.md
```

Struttura consigliata:

```markdown
# Report UD04 – Primo servizio osservabile

## Avvio servizio
- porta usata:
- comando di avvio:

## Endpoint verificati
- /health:
- /ready:
- /metrics:
- /work:
- /fail:

## Correlazione request-id
- request-id usato:
- comando curl:
- riga di log trovata:

## SLI calcolati
- total_requests:
- error_rate_percent:
- availability_percent:
- latency_p50_ms:
- latency_p95_ms:

## Interpretazione
- cosa indica error_rate:
- cosa indica p95:
- quale alert avrebbe senso impostare:

## Problemi incontrati e correzioni
```

## 14. Verifica automatica

Possiamo eseguire lo script di verifica:

```bash
src/verifica_ud04.sh
```

Lo script usa una porta di test, avvia il servizio, genera alcune richieste, calcola un report SLI e verifica che gli output principali siano presenti.

## 15. Commit finale

Prima controlliamo lo stato:

```bash
git status
```

Aggiungiamo solo file utili:

```bash
git add README.md 00_OBS_UD04_Concetti.md 01_OBS_UD04_LAB_guidato_Primo_Servizio_Osservabile.md
git add 02_OBS_UD04_BRIEFING_DOCENTE_POMERIGGIO.md 03_OBS_UD04_LAB_autonomo_SLI_RequestID_Report.md
git add DOCENTE_Q\&A_OBS_UD04_Primo_Servizio_Osservabile.md
git add src config docs/report_ud04.md evidence/sli_report.json .gitignore
```

Commit:

```bash
git commit -m "[OBS_UD04] primo servizio osservabile"
git push
```

## 16. Criteri di completamento

La UD04 è completata quando:

- il servizio parte senza errori;
- `/health` risponde `200`;
- `/ready` risponde `200` in modalità normale e `503` quando `READY=false`;
- `/metrics` mostra valori aggiornati;
- `logs/app.log` contiene log JSON validi;
- almeno un `request_id` è correlato tra risposta e log;
- `evidence/sli_report.json` contiene gli indicatori richiesti;
- `docs/report_ud04.md` contiene interpretazione tecnica;
- il lavoro è stato versionato con commit coerente.

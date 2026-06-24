# OBS_UD04 – Laboratorio autonomo: SLI, request-id e report tecnico

## Scenario

Nel laboratorio guidato abbiamo costruito e avviato un servizio osservabile. Ora lavoriamo in autonomia su tre scenari:

1. traffico normale;
2. traffico con errori;
3. traffico con lentezza controllata.

Per ogni scenario dobbiamo raccogliere evidenze, calcolare SLI e scrivere un breve report tecnico.

## Obiettivo

Al termine del laboratorio autonomo dobbiamo produrre:

```text
docs/report_ud04.md
evidence/sli_report.json
```

Il report deve dimostrare che sappiamo collegare richieste HTTP, log JSON, request-id, metriche e indicatori operativi.

## 1. Preparazione ambiente

Posizioniamoci nella cartella della UD04.

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD04_Primo_Servizio_Osservabile
pwd
```

Puliamo i file runtime precedenti se vogliamo partire da una baseline nuova:

```bash
mkdir -p logs evidence docs
: > logs/app.log
```

Avviamo il servizio in un terminale dedicato:

```bash
PORT=9100 READY=true LOG_PATH="logs/app.log" python3 src/observable_service.py
```

Apriamo un secondo terminale nella stessa cartella.

## 2. Scenario A – baseline

Generiamo poche richieste prevalentemente positive:

```bash
curl -i -H 'X-Request-Id: auto-baseline-001' http://localhost:9100/health
curl -i -H 'X-Request-Id: auto-baseline-002' http://localhost:9100/ready
curl -i -H 'X-Request-Id: auto-baseline-003' http://localhost:9100/time
curl -i -H 'X-Request-Id: auto-baseline-004' 'http://localhost:9100/work?ms=50'
```

Verifichiamo i log:

```bash
grep 'auto-baseline' logs/app.log
```

Annotiamo nel report:

- quali endpoint sono stati chiamati;
- quali status code abbiamo ottenuto;
- quale request-id abbiamo ritrovato nei log.

## 3. Scenario B – errori controllati

Generiamo errori applicativi e richieste non valide.

```bash
curl -i -H 'X-Request-Id: auto-error-500' http://localhost:9100/fail
curl -i -H 'X-Request-Id: auto-error-404' http://localhost:9100/nope
curl -i -X POST -H 'X-Request-Id: auto-error-400' -H 'Content-Type: application/json' -d '{"msg":' http://localhost:9100/echo
```

Cerchiamo le righe:

```bash
grep 'auto-error' logs/app.log
```

Annotiamo nel report:

- quali errori sono stati generati;
- quali status code corrispondono ai diversi casi;
- quale differenza osserviamo tra errore 400, 404 e 500.

## 4. Scenario C – lentezza controllata

Generiamo richieste con latenza crescente.

```bash
curl -i -H 'X-Request-Id: auto-slow-100' 'http://localhost:9100/work?ms=100'
curl -i -H 'X-Request-Id: auto-slow-300' 'http://localhost:9100/work?ms=300'
curl -i -H 'X-Request-Id: auto-slow-700' 'http://localhost:9100/work?ms=700'
```

Verifichiamo le latenze nel log:

```bash
grep 'auto-slow' logs/app.log
```

Annotiamo nel report:

- quali richieste sono state lente;
- come cambia `duration_ms`;
- perché p95 può evidenziare problemi non visibili guardando solo la media.

## 5. Generazione traffico aggiuntivo

Eseguiamo lo script automatico:

```bash
src/generate_traffic.sh 9100 50
```

Verifichiamo:

```bash
wc -l logs/app.log
tail -n 5 logs/app.log
```

## 6. Calcolo report SLI

Eseguiamo il parser:

```bash
python3 src/parse_sli.py logs/app.log evidence/sli_report.json
```

Visualizziamo il report:

```bash
cat evidence/sli_report.json | python3 -m json.tool
```

## 7. Correlazione request-id

Scegliamo due request-id e documentiamo le righe di log.

Esempio:

```bash
grep 'auto-baseline-001' logs/app.log
grep 'auto-error-500' logs/app.log
```

Nel report dobbiamo inserire:

```markdown
## Correlazione request-id

### Esempio 1
- request-id:
- comando curl:
- status code:
- riga di log:

### Esempio 2
- request-id:
- comando curl:
- status code:
- riga di log:
```

## 8. Scrittura report tecnico

Creiamo:

```bash
nano docs/report_ud04.md
```

Usiamo questa struttura:

```markdown
# Report UD04 – Primo servizio osservabile

## Ambiente
- porta usata:
- comando di avvio:
- file log:

## Scenario A – baseline
- comandi eseguiti:
- risultati:
- evidenze:

## Scenario B – errori controllati
- comandi eseguiti:
- status osservati:
- righe di log rilevanti:

## Scenario C – lentezza controllata
- comandi eseguiti:
- latenze osservate:
- interpretazione:

## SLI
Riportare i valori principali da evidence/sli_report.json:
- total_requests:
- error_rate_percent:
- availability_percent:
- latency_p50_ms:
- latency_p95_ms:
- top_paths:

## Interpretazione operativa
- cosa ci dice error_rate:
- cosa ci dice p95:
- quale alert avrebbe senso impostare:
- quale campo aggiungeremmo ai log in un sistema reale:

## Problemi incontrati
- problema:
- ipotesi:
- test:
- correzione:
```

## 9. Verifica finale

Eseguiamo:

```bash
src/verifica_ud04.sh
```

Controlliamo lo stato Git:

```bash
git status
```

## 10. Commit

Aggiungiamo gli output versionabili:

```bash
git add docs/report_ud04.md evidence/sli_report.json
```

Se abbiamo modificato script o configurazioni:

```bash
git add src config README.md *.md .gitignore
```

Commit:

```bash
git commit -m "[OBS_UD04] SLI request-id e report tecnico"
git push
```

## 11. Criteri di completamento

Il laboratorio autonomo è completato quando:

- il servizio è stato eseguito correttamente;
- sono stati prodotti log JSON;
- sono stati documentati tre scenari;
- sono stati correlati almeno due request-id;
- `evidence/sli_report.json` è presente e leggibile;
- `docs/report_ud04.md` contiene interpretazione tecnica;
- il lavoro è stato versionato.

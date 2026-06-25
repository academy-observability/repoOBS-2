# OBS_UD04 - Svolgimento laboratorio autonomo potenziato

## 1. Scopo dello svolgimento

Questo file mostra uno svolgimento possibile del laboratorio autonomo potenziato UD04.

La sequenza e' stata verificata su una copia pulita della UD04. I valori numerici del report SLI possono cambiare in base alla macchina, al numero di richieste generate e allo stato iniziale del log.

---

## 2. Preparazione ambiente

Entriamo nella cartella UD04:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD04_Primo_Servizio_Osservabile
pwd
```

Prepariamo ambiente pulito:

```bash
mkdir -p logs evidence docs
: > logs/app.log
chmod 755 src/generate_traffic.sh src/verifica_ud04.sh
```

Avviamo il servizio in un primo terminale:

```bash
PORT=9100 READY=true LOG_PATH="logs/app.log" python3 src/observable_service.py
```

In un secondo terminale verifichiamo:

```bash
curl -i http://localhost:9100/health
```

Risultato atteso:

```text
HTTP/1.0 200 OK
```

---

## 3. Generazione traffico normale

Generiamo richieste positive a `/health`:

```bash
for i in $(seq 1 8); do
  curl -s -i -H "X-Request-Id: pot-health-${i}" http://localhost:9100/health > /dev/null
done
```

Generiamo richieste a `/ready`:

```bash
for i in $(seq 1 4); do
  curl -s -i -H "X-Request-Id: pot-ready-${i}" http://localhost:9100/ready > /dev/null
done
```

Generiamo richieste a `/time`:

```bash
for i in $(seq 1 4); do
  curl -s -i -H "X-Request-Id: pot-time-${i}" http://localhost:9100/time > /dev/null
done
```

Verifichiamo alcune righe:

```bash
grep 'pot-health-1' logs/app.log | python3 -m json.tool
grep 'pot-ready-1' logs/app.log | python3 -m json.tool
```

Interpretazione:

```text
Le richieste positive producono status 200 e level INFO.
I request-id scelti dal client compaiono nel log.
```

---

## 4. Generazione richieste lente

Generiamo richieste a `/work` con durate diverse:

```bash
for ms in 50 80 100 150 200 300 500 700 900 1200; do
  curl -s -i -H "X-Request-Id: pot-work-${ms}" "http://localhost:9100/work?ms=${ms}" > /dev/null
done
```

Verifichiamo una richiesta lenta:

```bash
grep 'pot-work-1200' logs/app.log | python3 -m json.tool
```

Campi da osservare:

```text
path = /work
query = ms=1200
status = 200
duration_ms vicino a 1200
simulated_delay_ms = 1200
```

Interpretazione:

```text
Il servizio risponde correttamente, ma alcune richieste sono lente.
Questo scenario impatta la latenza, non necessariamente l'availability.
```

---

## 5. Generazione errori 500

Generiamo errori applicativi simulati:

```bash
for i in $(seq 1 3); do
  curl -s -i -H "X-Request-Id: pot-fail-${i}" http://localhost:9100/fail > /dev/null
done
```

Verifichiamo:

```bash
grep 'pot-fail-1' logs/app.log | python3 -m json.tool
```

Interpretazione:

```text
/fail produce status 500.
Nel log il level e' ERROR e il campo error vale simulated_failure.
```

---

## 6. Generazione errori 404

Generiamo richieste verso endpoint inesistente:

```bash
for i in $(seq 1 3); do
  curl -s -i -H "X-Request-Id: pot-missing-${i}" http://localhost:9100/nope > /dev/null
done
```

Verifichiamo:

```bash
grep 'pot-missing-1' logs/app.log | python3 -m json.tool
```

Interpretazione:

```text
/nope produce status 404.
Il servizio ha risposto, ma l'endpoint richiesto non esiste.
```

---

## 7. Generazione errori 400

Generiamo richieste POST con JSON malformato:

```bash
for i in $(seq 1 3); do
  curl -s -i \
    -X POST \
    -H "X-Request-Id: pot-badjson-${i}" \
    -H 'Content-Type: application/json' \
    -d '{"msg":' \
    http://localhost:9100/echo > /dev/null
done
```

Verifichiamo:

```bash
grep 'pot-badjson-1' logs/app.log | python3 -m json.tool
```

Interpretazione:

```text
Il servizio riceve una richiesta con body JSON non valido.
Risponde con status 400 e level WARN.
```

---

## 8. Generazione POST validi

Generiamo anche alcune richieste POST corrette:

```bash
for i in $(seq 1 3); do
  curl -s -i \
    -X POST \
    -H "X-Request-Id: pot-echo-${i}" \
    -H 'Content-Type: application/json' \
    -d '{"msg":"ok"}' \
    http://localhost:9100/echo > /dev/null
done
```

Verifichiamo:

```bash
grep 'pot-echo-1' logs/app.log | python3 -m json.tool
```

Interpretazione:

```text
La stessa rotta /echo puo' produrre 200 o 400.
La differenza dipende dalla validita' del JSON inviato.
```

---

## 9. Controllo del log

Verifichiamo il numero di righe:

```bash
wc -l logs/app.log
```

Con la sequenza proposta dovremmo avere almeno 30 righe. Nella prova verificata sono state generate 39 richieste.

Visualizziamo le ultime righe:

```bash
tail -n 5 logs/app.log
```

Formattiamo una singola riga:

```bash
tail -n 1 logs/app.log | python3 -m json.tool
```

---

## 10. Calcolo degli SLI

Eseguiamo il parser:

```bash
python3 src/parse_sli.py logs/app.log evidence/sli_report.json
```

Visualizziamo il report:

```bash
cat evidence/sli_report.json | python3 -m json.tool
```

Esempio di valori ottenuti nella prova:

```json
{
    "total_requests": 39,
    "error_count": 9,
    "error_rate_percent": 23.08,
    "availability_percent": 76.92,
    "latency_p50_ms": 0,
    "latency_p95_ms": 702,
    "latency_max_ms": 1202,
    "status_breakdown": {
        "200": 30,
        "500": 3,
        "404": 3,
        "400": 3
    }
}
```

Esempio di `top_paths` ottenuto nella prova:

```json
[
    {
        "path": "/work",
        "count": 10
    },
    {
        "path": "/health",
        "count": 9
    },
    {
        "path": "/echo",
        "count": 6
    },
    {
        "path": "/ready",
        "count": 4
    },
    {
        "path": "/time",
        "count": 4
    }
]
```

---

## 11. Individuazione endpoint piu problematico

Analizzando i dati:

- `/work` e' l'endpoint piu chiamato;
- `/work` introduce le latenze maggiori;
- `/fail` produce errori 500;
- `/echo` produce sia 200 sia 400, a seconda della validita' del JSON;
- `/nope` produce 404, ma non e' un endpoint reale del servizio.

Conclusione possibile:

```text
L'endpoint piu rilevante per la latenza e' /work.
L'endpoint /fail e' il piu problematico dal punto di vista degli errori server, ma nel laboratorio e' un errore intenzionale.
In un sistema reale, controllerei prima /work per la latenza p95 e poi gli endpoint con status 500.
```

---

## 12. Alert proposti

### Alert 1 - Error rate

```text
SLI: error_rate_percent
Soglia proposta: > 5%
```

Motivazione:

```text
Un error rate superiore al 5% indica una quota significativa di richieste fallite.
Nel test l'error rate e' molto piu alto perche abbiamo generato errori intenzionali.
```

Azione:

```text
Controllare status_breakdown, endpoint coinvolti e log con level ERROR/WARN.
```

### Alert 2 - Latenza p95

```text
SLI: latency_p95_ms
Soglia proposta: > 500 ms
```

Motivazione:

```text
La p95 sopra 500 ms indica che una parte significativa delle richieste peggiori e' lenta.
Nel test la p95 cresce per effetto delle chiamate /work?ms=700, /work?ms=900 e /work?ms=1200.
```

Azione:

```text
Analizzare endpoint lenti, parametri di query e durata registrata in duration_ms.
```

---

## 13. Miglioramento proposto ai log

Campo proposto:

```text
environment
```

Utilita':

```text
Permetterebbe di distinguere log di sviluppo, test, staging e produzione.
In una piattaforma centralizzata aiuterebbe a evitare confronti sbagliati tra ambienti diversi.
```

Possibile attenzione:

```text
Il campo non contiene dati personali, quindi ha basso rischio privacy.
Bisogna pero' mantenere valori standardizzati, per esempio dev, test, staging, prod.
```

Altro campo utile:

```text
trace_id
```

Utilita':

```text
Servirebbe a collegare la stessa richiesta tra piu servizi, non solo dentro un singolo processo.
```

---

## 14. Scrittura del report

Creiamo:

```bash
nano docs/report_ud04.md
```

Esempio di contenuto:

```markdown
# Report UD04 - Laboratorio autonomo potenziato

## Ambiente
- porta: 9100
- comando di avvio: `PORT=9100 READY=true LOG_PATH="logs/app.log" python3 src/observable_service.py`
- file log: `logs/app.log`

## Traffico generato
- richieste totali generate: 39
- endpoint usati: `/health`, `/ready`, `/time`, `/work`, `/fail`, `/nope`, `/echo`
- convenzione request-id: prefisso `pot-`

## Errori provocati
- 400: POST `/echo` con JSON malformato
- 404: GET `/nope`
- 500: GET `/fail`
- interpretazione: gli errori hanno cause diverse e non vanno letti tutti nello stesso modo.

## Latenza
- richieste lente generate su `/work`
- valori usati: 50, 80, 100, 150, 200, 300, 500, 700, 900, 1200 ms
- interpretazione: p95 cresce quando introduciamo richieste lente.

## SLI
- total_requests: 39
- error_count: 9
- error_rate_percent: 23.08
- availability_percent: 76.92
- latency_p50_ms: 0
- latency_p95_ms: 702
- latency_max_ms: 1202
- status_breakdown: 200=30, 400=3, 404=3, 500=3
- top_paths: `/work`, `/health`, `/echo`

## Endpoint piu problematico
- endpoint per latenza: `/work`
- endpoint per errori server: `/fail`
- evidenze: `latency_p95_ms`, `latency_max_ms`, `status_breakdown`
- interpretazione: `/work` mostra degrado di latenza; `/fail` genera errori intenzionali.

## Alert proposti

### Alert 1 - Error rate
- soglia: `error_rate_percent > 5%`
- motivazione: quota significativa di richieste fallite
- azione: controllare status e log ERROR/WARN

### Alert 2 - Latenza p95
- soglia: `latency_p95_ms > 500`
- motivazione: richieste peggiori frequenti troppo lente
- azione: analizzare endpoint `/work` e parametri `ms`

## Miglioramento dei log
- campo proposto: `environment`
- utilita': distinguere dev, test, staging e produzione
- attenzione privacy/sicurezza: basso rischio, ma valori da standardizzare

## Conclusione
Il servizio produce segnali osservabili utili: log JSON, request-id, status code, durate e SLI.
I dati permettono di distinguere errori applicativi, richieste non valide, endpoint inesistenti e problemi di latenza.
```

Adattare i valori ai risultati effettivamente ottenuti.

---

## 15. Verifica finale

Verifichiamo i file:

```bash
test -s docs/report_ud04.md && echo "report presente"
test -s evidence/sli_report.json && echo "report SLI presente"
python3 -m json.tool evidence/sli_report.json > /dev/null && echo "JSON valido"
```

Eseguiamo anche:

```bash
src/verifica_ud04.sh
```

---

## 16. Commit

Controlliamo:

```bash
git status
```

Aggiungiamo gli output:

```bash
git add docs/report_ud04.md evidence/sli_report.json
```

Commit:

```bash
git commit -m "[OBS_UD04] laboratorio autonomo potenziato completato"
git push
```

---

## 17. Nota finale

I valori numerici possono essere diversi da quelli riportati nello svolgimento.

La parte importante e' che il report dimostri il ragionamento:

```text
richieste generate -> log prodotti -> SLI calcolati -> interpretazione operativa -> alert proposti
```

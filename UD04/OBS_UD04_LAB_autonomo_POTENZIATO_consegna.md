# OBS_UD04 - Laboratorio autonomo potenziato: analisi operativa di un servizio osservabile

## 1. Obiettivo del laboratorio

In questo laboratorio autonomo non dobbiamo semplicemente ripetere i comandi del laboratorio guidato. Dobbiamo usare il servizio UD04 come oggetto di analisi operativa.

L'obiettivo e' dimostrare di saper:

- generare traffico controllato;
- provocare errori diversi;
- introdurre richieste lente;
- correlare risposte HTTP e log tramite `request_id`;
- calcolare SLI;
- interpretare i dati ottenuti;
- proporre alert sensati;
- individuare quali informazioni mancano nei log per un sistema reale.

Output richiesti:

```text
docs/report_ud04.md
evidence/sli_report.json
```

---

## 2. Preparazione ambiente

Posizionarsi nella cartella della UD04:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD04_Primo_Servizio_Osservabile
pwd
```

Preparare le directory e pulire il log runtime:

```bash
mkdir -p logs evidence docs
: > logs/app.log
```

Rendere eseguibili gli script:

```bash
chmod 755 src/generate_traffic.sh src/verifica_ud04.sh
```

Avviare il servizio in un terminale dedicato:

```bash
PORT=9100 READY=true LOG_PATH="logs/app.log" python3 src/observable_service.py
```

Aprire un secondo terminale nella stessa cartella e verificare:

```bash
curl -i http://localhost:9100/health
```

---

## 3. Richiesta 1 - Generare almeno 30 richieste scelte autonomamente

Generare almeno 30 richieste HTTP scegliendo autonomamente una combinazione di endpoint.

Devono essere presenti almeno:

- richieste a `/health`;
- richieste a `/ready`;
- richieste a `/time`;
- richieste a `/work?ms=...`;
- richieste POST a `/echo`.

Ogni richiesta significativa deve usare un `X-Request-Id` riconoscibile.

Esempio di convenzione:

```text
pot-health-1
pot-ready-1
pot-work-300
pot-echo-1
```

Nel report indicare:

- quanti endpoint sono stati chiamati;
- quali endpoint sono stati chiamati piu spesso;
- quali request-id sono stati usati come esempi.

---

## 4. Richiesta 2 - Provocare almeno tre tipi diversi di errore

Generare almeno tre tipi di errore:

| Errore | Come provocarlo | Significato |
|---|---|---|
| 400 | POST `/echo` con JSON malformato | richiesta non valida |
| 404 | endpoint inesistente, per esempio `/nope` | rotta non trovata |
| 500 | endpoint `/fail` | errore applicativo simulato |

Nel report spiegare la differenza tra:

- errore client;
- endpoint inesistente;
- errore lato servizio.

---

## 5. Richiesta 3 - Introdurre richieste lente

Generare richieste a `/work` con latenze diverse.

Esempi:

```text
/work?ms=50
/work?ms=100
/work?ms=300
/work?ms=700
/work?ms=1200
```

Nel report spiegare:

- come cambia `duration_ms`;
- perche un servizio puo' essere disponibile ma lento;
- perche `latency_p95_ms` puo' essere piu utile della sola media.

---

## 6. Richiesta 4 - Calcolare e interpretare gli SLI

Eseguire il parser:

```bash
python3 src/parse_sli.py logs/app.log evidence/sli_report.json
```

Visualizzare il report:

```bash
cat evidence/sli_report.json | python3 -m json.tool
```

Nel report `docs/report_ud04.md` riportare e interpretare almeno:

- `total_requests`;
- `error_count`;
- `error_rate_percent`;
- `availability_percent`;
- `latency_p50_ms`;
- `latency_p95_ms`;
- `latency_max_ms`;
- `status_breakdown`;
- `top_paths`.

---

## 7. Richiesta 5 - Individuare l'endpoint piu problematico

Usando `status_breakdown`, `top_paths` e le righe di log, individuare quale endpoint appare piu problematico.

Nel report spiegare:

- se il problema principale e' legato agli errori;
- se il problema principale e' legato alla latenza;
- quale endpoint richiederebbe una verifica ulteriore;
- quale dato del log supporta questa conclusione.

---

## 8. Richiesta 6 - Proporre almeno due alert

Proporre almeno due alert:

| Alert | Esempio |
|---|---|
| Alert su error rate | `error_rate_percent > 5%` |
| Alert su latenza p95 | `latency_p95_ms > 500` |

Per ogni alert indicare:

- metrica o SLI osservato;
- soglia proposta;
- motivazione;
- possibile azione operativa.

---

## 9. Richiesta 7 - Proporre un miglioramento dei log

Indicare almeno un campo che sarebbe utile aggiungere ai log in un sistema reale.

Esempi:

| Campo | Perche potrebbe servire |
|---|---|
| `user_id` | capire quali utenti sono impattati |
| `tenant_id` | distinguere clienti o ambienti diversi |
| `environment` | distinguere dev, test, produzione |
| `trace_id` | collegare richieste tra piu servizi |
| `host` | capire su quale macchina o container e' avvenuto l'evento |
| `region` | identificare problemi localizzati geograficamente |

Nel report spiegare:

- quale campo aggiungeremmo;
- quale domanda operativa permetterebbe di rispondere;
- quale rischio privacy/sicurezza potrebbe introdurre.

---

## 10. Struttura richiesta del report

Creare:

```bash
nano docs/report_ud04.md
```

Struttura minima:

```markdown
# Report UD04 - Laboratorio autonomo potenziato

## Ambiente
- porta:
- comando di avvio:
- file log:

## Traffico generato
- numero richieste:
- endpoint usati:
- convenzione request-id:

## Errori provocati
- 400:
- 404:
- 500:
- interpretazione:

## Latenza
- richieste lente generate:
- valori osservati in `duration_ms`:
- interpretazione p50/p95/max:

## SLI
- total_requests:
- error_count:
- error_rate_percent:
- availability_percent:
- latency_p50_ms:
- latency_p95_ms:
- latency_max_ms:
- status_breakdown:
- top_paths:

## Endpoint piu problematico
- endpoint:
- evidenze:
- interpretazione:

## Alert proposti
### Alert 1 - Error rate
- soglia:
- motivazione:
- azione:

### Alert 2 - Latenza p95
- soglia:
- motivazione:
- azione:

## Miglioramento dei log
- campo proposto:
- utilita':
- attenzione privacy/sicurezza:

## Conclusione
- cosa dimostrano i dati raccolti:
- quale controllo farei come passo successivo:
```

---

## 11. Verifica finale

Eseguire:

```bash
src/verifica_ud04.sh
```

Controllare che i file richiesti esistano:

```bash
test -s docs/report_ud04.md && echo "report presente"
test -s evidence/sli_report.json && echo "report SLI presente"
python3 -m json.tool evidence/sli_report.json > /dev/null && echo "JSON valido"
```

---

## 12. Commit

Controllare lo stato:

```bash
git status
```

Aggiungere solo gli output versionabili:

```bash
git add docs/report_ud04.md evidence/sli_report.json
```

Commit:

```bash
git commit -m "[OBS_UD04] laboratorio autonomo potenziato completato"
git push
```

---

## 13. Criteri di completamento

Il laboratorio e' completato quando:

- sono state generate almeno 30 richieste;
- sono presenti errori 400, 404 e 500;
- sono presenti richieste lente;
- `evidence/sli_report.json` e' stato generato;
- `docs/report_ud04.md` interpreta i dati, non li copia soltanto;
- sono stati proposti almeno due alert;
- e' stato proposto almeno un miglioramento dei log;
- il lavoro e' stato versionato.

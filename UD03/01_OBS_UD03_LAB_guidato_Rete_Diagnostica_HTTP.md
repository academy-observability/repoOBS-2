# OBS_UD03 – Laboratorio guidato: rete, diagnostica e HTTP

## 1. Obiettivo del laboratorio guidato

In questo laboratorio lavoriamo insieme su una sequenza controllata di test di rete e HTTP.

L'obiettivo è imparare a distinguere:

- problema di rete;
- problema DNS;
- problema di porta;
- servizio non avviato;
- endpoint HTTP errato;
- porta già occupata;
- errore applicativo simulato.

Alla fine prepariamo una prima evidenza tecnica in `docs/evidence_ud03.md`.

---

## 2. Posizionamento nella directory della UD

Portiamoci nella cartella della UD:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD03_Rete_Diagnostica_HTTP
pwd
ls -la
```

Se il corso viene distribuito in una struttura diversa, usiamo la cartella indicata dal docente.

Verifichiamo la presenza delle directory principali:

```bash
ls -la src config docs logs evidence
```

---

## 3. Verifica strumenti

Eseguiamo:

```bash
which ip || true
which ping || true
which curl || true
which ss || true
which python3 || true
which dig || true
which nslookup || true
which traceroute || true
which tracepath || true
python3 --version
```

Se mancano alcuni strumenti su Ubuntu/WSL, il docente può guidare l'installazione:

```bash
sudo apt update
sudo apt install -y iproute2 iputils-ping curl dnsutils traceroute iputils-tracepath netcat-openbsd
```

> Nota: non tutti gli ambienti consentono `ping`, `traceroute` o l'installazione di pacchetti. In quel caso lavoriamo con gli strumenti disponibili e annotiamo il limite nell'evidenza.

---

## 4. Preparazione file evidenza

Creiamo il file di evidenza:

```bash
mkdir -p docs logs
cat > docs/evidence_ud03.md <<'EOF'
# OBS_UD03 – Evidence: rete, diagnostica e HTTP

## 1. Snapshot rete

## 2. Baseline IP, DNS e HTTP

## 3. Scenario guidato A – servizio locale raggiungibile

## 4. Scenario guidato B – endpoint non esistente, HTTP 404

## 5. Scenario guidato C – porta non in ascolto

## 6. Scenario guidato D – porta già occupata

## 7. Scenario guidato E – lettura curl verbose

## 8. Sintesi diagnostica

## 9. Problemi incontrati e soluzioni
EOF
```

Controlliamo:

```bash
sed -n '1,120p' docs/evidence_ud03.md
```

---

## 5. Snapshot rete iniziale

Usiamo lo script già fornito:

```bash
chmod +x src/net_snapshot.sh
./src/net_snapshot.sh
```

Lo script crea:

```text
logs/net_snapshot_ud03.txt
```

Controlliamo il file:

```bash
wc -l logs/net_snapshot_ud03.txt
head -n 30 logs/net_snapshot_ud03.txt
tail -n 30 logs/net_snapshot_ud03.txt
```

Aggiungiamo un riassunto all'evidenza:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Output sintetico snapshot

```text
Inserire qui 10-20 righe significative da logs/net_snapshot_ud03.txt: interfacce, route, DNS e porte in ascolto.
```
EOF
```

> Non dobbiamo committare il file in `logs/`: serve come output runtime locale.

---

## 6. Baseline: IP, DNS, HTTP

### 6.1 Test IP diretto

Eseguiamo:

```bash
ping -c 2 1.1.1.1
```

Se `ping` è bloccato o non disponibile, annotiamo il problema e proseguiamo.

### 6.2 Test DNS

Eseguiamo una delle due opzioni:

```bash
dig +short example.com
```

oppure:

```bash
nslookup example.com
```

### 6.3 Test HTTP

Eseguiamo:

```bash
curl -I https://example.com | head -n 10
```

Aggiungiamo una sintesi all'evidenza:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Interpretazione baseline

- `ping` verso IP verifica principalmente la raggiungibilità IP.
- `dig` o `nslookup` verifica la risoluzione DNS.
- `curl -I` verifica DNS, connessione, TLS nel caso HTTPS e risposta HTTP.
EOF
```

---

## 7. Avvio del server HTTP locale

Usiamo il server Python fornito nel laboratorio.

Apriamo un primo terminale nella cartella della UD ed eseguiamo:

```bash
python3 src/http_lab_server.py 8081
```

Il server rimane in esecuzione.

Apriamo un secondo terminale nella stessa cartella:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD03_Rete_Diagnostica_HTTP
```

Verifichiamo la porta:

```bash
ss -ltnp | grep 8081 || true
```

Dovremmo vedere una riga con `python3` in ascolto sulla porta `8081`.

---

## 8. Scenario guidato A – servizio locale raggiungibile

Dal secondo terminale eseguiamo:

```bash
curl -i http://localhost:8081/
```

Dovremmo ottenere una risposta simile:

```text
HTTP/1.0 200 OK
Content-Type: text/plain; charset=utf-8

OBS UD03 HTTP lab server
```

Proviamo anche:

```bash
curl -i http://localhost:8081/health
```

Risposta attesa:

```text
HTTP/1.0 200 OK
...
OK
```

Aggiungiamo all'evidenza:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Scenario guidato A – servizio locale raggiungibile

Sintomo: dobbiamo verificare se il servizio locale risponde sulla porta 8081.
Ipotesi: il processo Python è in ascolto sulla porta 8081.
Test: `ss -ltnp | grep 8081`, `curl -i http://localhost:8081/`, `curl -i http://localhost:8081/health`.
Interpretazione: se otteniamo HTTP 200, la rete locale, la porta e il servizio sono funzionanti.
EOF
```

---

## 9. Scenario guidato B – endpoint non esistente, HTTP 404

Eseguiamo:

```bash
curl -i http://localhost:8081/non-esiste
```

Risposta attesa:

```text
HTTP/1.0 404 Not Found
...
not found
```

Questo è un punto importante: il server risponde, quindi la rete non è rotta. L'endpoint richiesto non esiste.

Aggiungiamo:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Scenario guidato B – endpoint non esistente

Sintomo: richiesta a `/non-esiste` restituisce HTTP 404.
Ipotesi: il servizio è raggiungibile, ma l'endpoint non esiste.
Test: `curl -i http://localhost:8081/non-esiste`.
Interpretazione: HTTP 404 non indica un problema di rete; indica una risorsa o rotta non trovata lato applicazione.
EOF
```

---

## 10. Scenario guidato C – porta non in ascolto

Eseguiamo una richiesta verso una porta dove non abbiamo avviato servizi:

```bash
curl -i --max-time 3 http://localhost:8099/ || true
```

Verifichiamo se la porta è in ascolto:

```bash
ss -ltnp | grep 8099 || true
```

Interpretazione attesa:

```text
curl fallisce perché nessun servizio ascolta sulla porta 8099.
```

Aggiungiamo:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Scenario guidato C – porta non in ascolto

Sintomo: richiesta verso `localhost:8099` fallisce.
Ipotesi: nessun processo ascolta sulla porta 8099.
Test: `curl --max-time 3 http://localhost:8099/`, `ss -ltnp | grep 8099`.
Interpretazione: se `ss` non mostra la porta, il problema è a livello di servizio/porta, non di endpoint HTTP.
EOF
```

---

## 11. Scenario guidato D – porta già occupata

Con il server ancora attivo su `8081`, proviamo ad avviare una seconda istanza sulla stessa porta.

Nel secondo terminale:

```bash
python3 src/http_lab_server.py 8081 || true
```

Errore atteso:

```text
OSError: [Errno 98] Address already in use
```

Verifichiamo:

```bash
ss -ltnp | grep 8081 || true
```

Aggiungiamo:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Scenario guidato D – porta già occupata

Sintomo: avvio di una seconda istanza sulla porta 8081 fallisce con `Address already in use`.
Ipotesi: la porta è già occupata dal primo processo server.
Test: `ss -ltnp | grep 8081`.
Interpretazione: il problema non è la rete esterna; è un conflitto locale di porta.
EOF
```

---

## 12. Scenario guidato E – lettura di curl verbose

Eseguiamo:

```bash
curl -v http://localhost:8081/ 2>&1 | head -n 40
```

Osserviamo righe come:

```text
* Host localhost:8081 was resolved.
* Trying 127.0.0.1:8081...
* Connected to localhost (127.0.0.1) port 8081
> GET / HTTP/1.1
< HTTP/1.0 200 OK
```

Annotiamo che `curl -v` permette di leggere il percorso della richiesta.

Aggiungiamo:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

### Scenario guidato E – curl verbose

Sintomo: vogliamo leggere le fasi della richiesta HTTP.
Ipotesi: `curl -v` mostra risoluzione host, tentativo di connessione, richiesta e risposta.
Test: `curl -v http://localhost:8081/`.
Interpretazione: il verbose aiuta a localizzare il livello in cui avviene il problema.
EOF
```

---

## 13. Scenario facoltativo – traceroute o tracepath

Se disponibile:

```bash
traceroute -n 1.1.1.1 | head -n 15
```

Oppure:

```bash
tracepath 1.1.1.1 | head -n 15
```

Da ricordare: asterischi o hop mancanti non indicano sempre un guasto. Alcuni router non rispondono a questo tipo di pacchetti.

---

## 14. Arresto del server locale

Torniamo nel terminale dove il server è in esecuzione e premiamo:

```text
CTRL+C
```

Verifichiamo che la porta sia libera:

```bash
ss -ltnp | grep 8081 || true
```

---

## 15. Sintesi diagnostica finale

Completiamo l'evidenza con una tabella:

```bash
cat >> docs/evidence_ud03.md <<'EOF'

## 8. Sintesi diagnostica

| Sintomo | Livello più probabile | Test utile |
|---|---|---|
| nome non risolve | DNS | `dig`, `nslookup`, `/etc/resolv.conf` |
| IP non raggiungibile | rete/routing/firewall | `ping`, `ip r`, `traceroute` |
| porta non risponde | servizio/porta | `curl`, `ss -ltnp` |
| `Address already in use` | conflitto porta locale | `ss -ltnp`, PID processo |
| HTTP 404 | endpoint applicativo | `curl -i`, log applicativo |
| HTTP 500 | errore applicativo | `curl -i`, log applicativo |

## 9. Problemi incontrati e soluzioni

Inserire qui eventuali problemi reali incontrati durante il laboratorio.
EOF
```

---

## 16. Verifica automatica minima

Eseguiamo lo script di verifica:

```bash
chmod +x src/verifica_ud03.sh
./src/verifica_ud03.sh
```

Lo script controlla la presenza dei file principali e di alcune sezioni dell'evidenza.

---

## 17. Commit e consegna

Controlliamo lo stato:

```bash
git status
```

Aggiungiamo solo i file richiesti:

```bash
git add docs/evidence_ud03.md
```

Se il docente richiede anche script e materiali della UD nel repository personale:

```bash
git add README.md 00_OBS_UD03_Concetti.md 01_OBS_UD03_LAB_guidato_Rete_Diagnostica_HTTP.md 02_OBS_UD03_BRIEFING_DOCENTE_POMERIGGIO.md 03_OBS_UD03_LAB_autonomo_Diagnostica_HTTP.md DOCENTE_Q&A_OBS_UD03_Rete_Diagnostica_HTTP.md src config docs evidence img
```

Commit:

```bash
git commit -m "[UD03] Diagnostica rete e HTTP completata"
git push
```

---

## 18. Criteri di completamento

La UD03 guidata è completata quando:

- abbiamo creato `docs/evidence_ud03.md`;
- abbiamo raccolto uno snapshot di rete;
- abbiamo eseguito baseline IP/DNS/HTTP;
- abbiamo avviato e interrogato il server HTTP locale;
- abbiamo distinto HTTP 200, HTTP 404, porta non in ascolto e porta occupata;
- abbiamo documentato la diagnosi con il formato sintomo → ipotesi → test → interpretazione;
- il commit è presente nel repository remoto.

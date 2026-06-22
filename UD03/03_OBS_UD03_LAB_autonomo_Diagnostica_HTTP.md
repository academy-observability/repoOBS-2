# OBS_UD03 – Laboratorio autonomo: diagnostica rete e HTTP

## 1. Obiettivo

Nel laboratorio autonomo dobbiamo applicare il metodo visto al mattino su scenari controllati ma meno guidati.

Il risultato atteso è un file:

```text
docs/evidence_ud03.md
```

completo, leggibile e basato su evidenze.

Non basta riportare i comandi. Per ogni scenario dobbiamo spiegare cosa abbiamo capito.

---

## 2. Metodo obbligatorio

Per ogni scenario usiamo questa struttura:

```text
Sintomo
Ipotesi
Test eseguiti
Output chiave
Interpretazione
Correzione o workaround
Evidenza salvata
```

La qualità principale richiesta è la classificazione corretta del problema.

---

## 3. Preparazione

Posizioniamoci nella cartella della UD:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD03_Rete_Diagnostica_HTTP
```

Creiamo o aggiorniamo il file evidenza:

```bash
mkdir -p docs logs
[ -f docs/evidence_ud03.md ] || cat > docs/evidence_ud03.md <<'EOF'
# OBS_UD03 – Evidence: rete, diagnostica e HTTP

## Laboratorio autonomo
EOF
```

Verifichiamo gli strumenti:

```bash
which curl
which ss
which python3
(which dig || which nslookup) || true
```

---

## 4. Scenario A – DNS con resolver diversi

### Attività

Eseguiamo almeno due test DNS confrontando il resolver predefinito e un resolver esplicito.

Opzione con `dig`:

```bash
dig +short example.com
dig @1.1.1.1 +short example.com
dig @127.0.0.1 +time=1 +tries=1 example.com || true
```

Opzione con `nslookup`:

```bash
nslookup example.com
nslookup example.com 1.1.1.1
nslookup example.com 127.0.0.1 || true
```

### Domande da rispondere nell'evidenza

- Il resolver predefinito risponde?
- Il resolver `1.1.1.1` risponde?
- Il resolver `127.0.0.1` risponde nel nostro ambiente?
- Il problema, se presente, è DNS o HTTP?

---

## 5. Scenario B – Server locale su porta personalizzata

Avviamo il server su una porta diversa da quella usata al mattino, per esempio `8085`.

Apriamo un terminale e lanciamo:

```bash
python3 src/http_lab_server.py 8085
```

In un secondo terminale:

```bash
curl -i http://localhost:8085/
curl -i http://localhost:8085/health
ss -ltnp | grep 8085 || true
```

### Domande da rispondere

- Quale processo ascolta sulla porta?
- Che status code riceviamo su `/`?
- Che status code riceviamo su `/health`?
- Quale livello del sistema abbiamo verificato?

---

## 6. Scenario C – Endpoint applicativi diversi

Con il server ancora attivo su `8085`, testiamo:

```bash
curl -i http://localhost:8085/metrics
curl -i http://localhost:8085/fail
curl -i http://localhost:8085/non-esiste
```

### Interpretazione attesa

| Endpoint | Significato |
|---|---|
| `/metrics` | servizio raggiungibile, risposta testuale con metriche semplici |
| `/fail` | servizio raggiungibile, errore applicativo simulato HTTP 500 |
| `/non-esiste` | servizio raggiungibile, endpoint non trovato HTTP 404 |

### Domande da rispondere

- Quale differenza c'è tra 404 e 500?
- In entrambi i casi la rete funziona?
- Quale comando dimostra che la porta è aperta?

---

## 7. Scenario D – Porta non in ascolto

Scegliamo una porta non usata, per esempio `8099`.

```bash
curl -i --max-time 3 http://localhost:8099/ || true
ss -ltnp | grep 8099 || true
```

### Domande da rispondere

- Che errore produce `curl`?
- `ss` mostra un processo in ascolto?
- Il problema è DNS, HTTP o servizio/porta?

---

## 8. Scenario E – Porta già occupata

Con il server attivo su `8085`, proviamo ad avviare una seconda istanza sulla stessa porta:

```bash
python3 src/http_lab_server.py 8085 || true
```

Poi:

```bash
ss -ltnp | grep 8085 || true
```

### Domande da rispondere

- Quale errore viene prodotto?
- Perché non possiamo avviare due server sulla stessa porta e stesso indirizzo?
- Come individuiamo il processo che occupa la porta?

---

## 9. Scenario F – Curl verbose

Eseguiamo:

```bash
curl -v http://localhost:8085/ 2>&1 | head -n 40
curl -v http://localhost:8085/fail 2>&1 | head -n 40
```

### Domande da rispondere

- In quale riga vediamo il tentativo di connessione?
- In quale riga vediamo la richiesta HTTP?
- In quale riga vediamo lo status code?
- Il verbose è utile anche quando il server risponde con errore applicativo?

---

## 10. Scenario G – Richiesta lenta controllata

Eseguiamo:

```bash
time curl -i http://localhost:8085/slow
```

### Domande da rispondere

- Il servizio è raggiungibile?
- Lo status code è di successo?
- Perché una richiesta lenta può comunque essere una criticità?
- In una piattaforma di Observability, quale segnale vorremmo vedere per questo caso?

---

## 11. Arresto del server

Torniamo nel terminale del server e premiamo:

```text
CTRL+C
```

Verifichiamo:

```bash
ss -ltnp | grep 8085 || true
```

---

## 12. Tabella finale obbligatoria

Nel file `docs/evidence_ud03.md` inseriamo una tabella finale simile:

```markdown
## Tabella finale di classificazione

| Scenario | Sintomo | Livello del problema | Test decisivo | Interpretazione |
|---|---|---|---|---|
| A | ... | DNS | ... | ... |
| B | ... | servizio/porta | ... | ... |
| C | ... | HTTP/applicazione | ... | ... |
| D | ... | porta non in ascolto | ... | ... |
| E | ... | conflitto locale porta | ... | ... |
| F | ... | analisi richiesta | ... | ... |
| G | ... | latenza applicativa | ... | ... |
```

---

## 13. Verifica finale

Eseguiamo:

```bash
chmod +x src/verifica_ud03.sh
./src/verifica_ud03.sh
```

Correggiamo eventuali problemi segnalati.

---

## 14. Commit

Controlliamo cosa stiamo versionando:

```bash
git status
```

Aggiungiamo l'evidenza:

```bash
git add docs/evidence_ud03.md
```

Commit:

```bash
git commit -m "[UD03] Laboratorio autonomo diagnostica HTTP completato"
git push
```

---

## 15. Criteri di completamento

Il laboratorio autonomo è completato quando:

- il file `docs/evidence_ud03.md` contiene gli scenari A-G;
- ogni scenario include interpretazione, non solo output;
- la tabella finale di classificazione è presente;
- non sono stati versionati file runtime in `logs/`;
- il commit è presente nel repository remoto.

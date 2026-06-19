# OBS_UD02 - Laboratorio guidato

## Permessi, processi e troubleshooting locale

## Scenario

Stiamo preparando una macchina Linux per eseguire piccoli servizi e script che useremo nelle prossime UD. Prima di introdurre container, servizi HTTP strutturati e strumenti di monitoraggio, dobbiamo saper diagnosticare tre problemi locali molto comuni:

```text
Permission denied
processo non responsivo
porta occupata
```

Lavoriamo in modo guidato e documentiamo ogni passaggio significativo.

---

## Obiettivi del laboratorio guidato

Al termine del laboratorio dobbiamo essere in grado di:

- interpretare permessi su file e directory;
- modificare permessi con `chmod` simbolico e ottale;
- distinguere utente, gruppo e altri;
- verificare utente e gruppi correnti;
- avviare e individuare processi in background;
- leggere PID, comando, tempo di esecuzione, CPU e memoria;
- inviare segnali a un processo;
- diagnosticare una porta occupata;
- produrre uno script Bash con validazione dell'input;
- salvare evidenze tecniche in Markdown.

---

## Prerequisiti

Usiamo Ubuntu in WSL, Linux nativo oppure una shell Linux equivalente.

Verifichiamo i comandi necessari:

```bash
which whoami id groups chmod stat ps pgrep kill sleep python3 curl
ss -V || true
python3 --version
```

Su Ubuntu/WSL, se necessario:

```bash
sudo apt update
sudo apt install -y procps coreutils iproute2 curl
```

Su macOS, se `ss` non è disponibile, useremo `lsof` negli step sulle porte.

---

## 1. Preparazione workspace

Posizioniamoci nella cartella della UD02 del nostro repository.

Esempio:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD02_Permessi_Processi_Troubleshooting
pwd
ls -la
```

Creiamo le cartelle di lavoro, se non sono già presenti:

```bash
mkdir -p logs/sandbox/{public,private,scripts,tmp}
mkdir -p docs evidence src
```

Verifichiamo:

```bash
find . -maxdepth 2 -type d | sort
```

---

## 2. Identità dell'utente corrente

Prima di analizzare i permessi dobbiamo sapere con quale identità stiamo lavorando.

Eseguiamo:

```bash
whoami
id
groups
umask
```

Creiamo il primo report guidato:

```bash
cat > docs/report_guidato_ud02.md << 'EOF'
# Report guidato UD02

## Identità utente

EOF
```

Aggiungiamo gli output principali:

```bash
{
  echo '```text'
  echo "whoami: $(whoami)"
  echo "id: $(id)"
  echo "groups: $(groups)"
  echo "umask: $(umask)"
  echo '```'
} >> docs/report_guidato_ud02.md
```

---

## 3. Creazione file e lettura dei permessi

Creiamo due file: uno pubblico e uno privato.

```bash
echo "contenuto pubblico" > logs/sandbox/public/readme.txt
echo "contenuto riservato" > logs/sandbox/private/secret.txt
```

Osserviamo permessi, owner e gruppo:

```bash
ls -l logs/sandbox/public/readme.txt logs/sandbox/private/secret.txt
stat logs/sandbox/private/secret.txt | head
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Permessi iniziali dei file

EOF

{
  echo '```text'
  ls -l logs/sandbox/public/readme.txt logs/sandbox/private/secret.txt
  echo '```'
} >> docs/report_guidato_ud02.md
```

---

## 4. Permessi simbolici: rimozione e ripristino della lettura

Rimuoviamo la lettura agli altri utenti sul file privato:

```bash
chmod o-r logs/sandbox/private/secret.txt
ls -l logs/sandbox/private/secret.txt
```

Nel nostro ambiente potremmo essere ancora proprietari del file e riuscire comunque a leggerlo. Questo è normale: `o-r` rimuove il permesso agli altri, non al proprietario.

Per vedere un caso più chiaro, rimuoviamo la lettura al proprietario:

```bash
chmod u-r logs/sandbox/private/secret.txt
cat logs/sandbox/private/secret.txt || true
```

Ripristiniamo il permesso:

```bash
chmod u+r logs/sandbox/private/secret.txt
cat logs/sandbox/private/secret.txt
```

Aggiungiamo una nota al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Prova permessi simbolici

Abbiamo rimosso e ripristinato il permesso di lettura sul file `secret.txt`.
Il sintomo atteso, quando manca il permesso necessario, è `Permission denied`.

EOF
```

---

## 5. Permessi ottali: file privato e script eseguibile

Impostiamo il file riservato a `600`:

```bash
chmod 600 logs/sandbox/private/secret.txt
ls -l logs/sandbox/private/secret.txt
```

Creiamo uno script senza permesso di esecuzione:

```bash
cat > logs/sandbox/scripts/hello.sh << 'EOF'
#!/usr/bin/env bash
echo "Script eseguito correttamente"
EOF

ls -l logs/sandbox/scripts/hello.sh
./logs/sandbox/scripts/hello.sh || true
```

Aggiungiamo il permesso di esecuzione:

```bash
chmod 755 logs/sandbox/scripts/hello.sh
ls -l logs/sandbox/scripts/hello.sh
./logs/sandbox/scripts/hello.sh
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Permessi ottali

- `600` su `secret.txt`: il proprietario può leggere e scrivere; gruppo e altri non hanno permessi.
- `755` su `hello.sh`: il proprietario può leggere, scrivere ed eseguire; gruppo e altri possono leggere ed eseguire.

EOF
```

---

## 6. Permessi sulle directory

Sulle directory il permesso `x` permette di attraversare il percorso.

Verifichiamo lo stato iniziale:

```bash
ls -ld logs/sandbox/private
ls logs/sandbox/private
```

Rimuoviamo temporaneamente il permesso di esecuzione al proprietario:

```bash
chmod u-x logs/sandbox/private
ls logs/sandbox/private || true
cat logs/sandbox/private/secret.txt || true
```

Ripristiniamo subito:

```bash
chmod u+x logs/sandbox/private
ls logs/sandbox/private
cat logs/sandbox/private/secret.txt
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Permessi sulle directory

Il permesso `x` su una directory permette di attraversare il percorso. Senza `x`, anche se conosciamo il nome di un file, possiamo avere errori di accesso.

EOF
```

---

## 7. Processi in background

Avviamo due processi `sleep` in background:

```bash
sleep 600 &
sleep 600 &
```

Individuiamoli:

```bash
ps -ef | grep sleep | grep -v grep
pgrep sleep
```

Salviamo il PID dell'ultimo processo `sleep`:

```bash
PID=$(pgrep -n sleep)
echo "$PID"
ps -p "$PID" -o pid,ppid,comm,etime,%cpu,%mem
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Processi sleep

EOF

{
  echo '```text'
  ps -p "$PID" -o pid,ppid,comm,etime,%cpu,%mem
  echo '```'
} >> docs/report_guidato_ud02.md
```

Terminiamo il processo selezionato in modo ordinato:

```bash
kill -15 "$PID"
sleep 1
ps -p "$PID" || true
```

Terminiamo eventuali processi `sleep` rimasti, usando PID specifici:

```bash
for p in $(pgrep sleep || true); do
  kill -15 "$p" || true
done
```

---

## 8. Processo che ignora SIGTERM

Ora usiamo uno script dimostrativo che ignora `SIGTERM`. Questo scenario è più realistico rispetto a un semplice `sleep`, perché `sleep` normalmente termina quando riceve `SIGTERM`.

Creiamo lo script:

```bash
cat > src/ignore_term.sh << 'EOF'
#!/usr/bin/env bash
trap 'echo "SIGTERM ricevuto ma ignorato"' TERM
echo "Processo dimostrativo avviato con PID $$"
while true; do
  sleep 5
done
EOF

chmod 755 src/ignore_term.sh
```

Avviamolo:

```bash
./src/ignore_term.sh > logs/sandbox/tmp/ignore_term.log 2>&1 &
DEMO_PID=$!
echo "$DEMO_PID"
sleep 1
ps -p "$DEMO_PID" -o pid,comm,etime,%cpu,%mem
```

Proviamo `SIGTERM`:

```bash
kill -15 "$DEMO_PID"
sleep 1
ps -p "$DEMO_PID" -o pid,comm,etime,%cpu,%mem || true
cat logs/sandbox/tmp/ignore_term.log
```

Il processo dovrebbe essere ancora attivo. Usiamo quindi `SIGKILL`:

```bash
kill -9 "$DEMO_PID"
sleep 1
ps -p "$DEMO_PID" || true
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## SIGTERM e SIGKILL

Abbiamo usato un processo dimostrativo che intercetta `SIGTERM` e continua a restare attivo.
In questo caso `SIGKILL` termina forzatamente il processo.

EOF
```

---

## 9. Porta occupata

Avviamo un piccolo server HTTP sulla porta `18080`.

```bash
python3 -m http.server 18080 --directory logs/sandbox/public > logs/sandbox/tmp/http_18080.log 2>&1 &
HTTP_PID=$!
sleep 1
echo "$HTTP_PID"
```

Verifichiamo che risponda:

```bash
curl -I http://localhost:18080 | head -n 1
```

Proviamo ad avviare un secondo server sulla stessa porta:

```bash
python3 -m http.server 18080 --directory logs/sandbox/public || true
```

Dovremmo ottenere un errore simile a:

```text
OSError: [Errno 98] Address already in use
```

Individuiamo il processo che usa la porta.

Su Linux:

```bash
ss -ltnp | grep 18080 || true
```

Su macOS:

```bash
lsof -iTCP:18080 -sTCP:LISTEN || true
```

Terminiamo solo il processo che abbiamo avviato:

```bash
kill -15 "$HTTP_PID"
sleep 1
ps -p "$HTTP_PID" || true
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Porta occupata

Abbiamo avviato un server HTTP sulla porta `18080` e poi provato ad avviare un secondo processo sulla stessa porta.
Il sintomo è `Address already in use`.
La verifica si esegue con `ss` su Linux oppure con `lsof` su macOS.

EOF
```

---

## 10. Script `proc_report.sh`

Creiamo uno script Bash che accetta un PID e restituisce informazioni essenziali sul processo.

```bash
cat > src/proc_report.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

PID="${1:-}"

if [[ -z "$PID" ]]; then
  echo "Usage: $0 <PID>" >&2
  exit 2
fi

if ! [[ "$PID" =~ ^[0-9]+$ ]]; then
  echo "PID must be a number" >&2
  exit 2
fi

if ! ps -p "$PID" > /dev/null 2>&1; then
  echo "PID $PID not found" >&2
  exit 2
fi

ps -p "$PID" -o pid,ppid,comm,etime,%cpu,%mem
EOF

chmod 755 src/proc_report.sh
```

Testiamo lo script:

```bash
sleep 300 &
TEST_PID=$!
./src/proc_report.sh "$TEST_PID"
./src/proc_report.sh abc || true
./src/proc_report.sh 999999 || true
kill -15 "$TEST_PID"
```

Aggiungiamo al report:

```bash
cat >> docs/report_guidato_ud02.md << 'EOF'

## Script proc_report.sh

Lo script `src/proc_report.sh` valida l'input, controlla che il PID esista e mostra un report sintetico del processo.

EOF
```

---

## 11. Evidenza guidata

Creiamo il file di evidenza della parte guidata:

```bash
cat > evidence/evidence_ud02_guidato.md << 'EOF'
# Evidence guidata UD02

## Attività completate

- Verifica identità utente con `whoami`, `id`, `groups`, `umask`.
- Analisi permessi file e directory con `ls -l`, `ls -ld`, `stat`.
- Uso di `chmod` simbolico e ottale.
- Avvio e identificazione processi con `sleep`, `ps`, `pgrep`.
- Test di `SIGTERM` e `SIGKILL` con processo dimostrativo.
- Diagnosi di porta occupata sulla porta `18080`.
- Creazione e test dello script `src/proc_report.sh`.

## File prodotti

- `docs/report_guidato_ud02.md`
- `evidence/evidence_ud02_guidato.md`
- `src/proc_report.sh`
- `src/ignore_term.sh`

## Nota finale

Il metodo usato nella UD02 segue la sequenza: sintomo, ipotesi, verifica, interpretazione, correzione, evidenza.
EOF
```

---

## 12. Verifica minima

Se presente, eseguiamo lo script di verifica:

```bash
chmod 755 src/verifica_ud02.sh
./src/verifica_ud02.sh
```

Lo script controlla solo la presenza minima dei file. Non sostituisce la valutazione del contenuto.

---

## 13. Commit finale della parte guidata

Controlliamo lo stato del repository:

```bash
git status
```

Aggiungiamo i file prodotti:

```bash
git add docs/report_guidato_ud02.md evidence/evidence_ud02_guidato.md src/proc_report.sh src/ignore_term.sh
```

Commit:

```bash
git commit -m "[OBS-UD02] Laboratorio guidato permessi processi troubleshooting"
```

Push:

```bash
git push
```

---

## Domande di consolidamento

1. Perché `chmod o-r file.txt` può non impedire al proprietario di leggere il file?
2. Che differenza c'è tra permesso `x` su file e permesso `x` su directory?
3. Perché `SIGTERM` è preferibile a `SIGKILL`?
4. Che cosa indica il PID?
5. Come possiamo individuare il processo che occupa una porta?
6. Perché è meglio terminare un PID specifico invece di usare comandi troppo generici?
7. Quale collegamento c'è tra questa UD e l'Observability?

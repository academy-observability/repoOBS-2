# OBS_UD02 - Laboratorio autonomo

## Diagnostica di permessi, processi e porta occupata

## Scenario

Nel laboratorio guidato abbiamo lavorato su permessi, processi, segnali e porte occupate seguendo passaggi assistiti.

Nel laboratorio autonomo simuliamo una piccola situazione operativa: un ambiente locale presenta tre problemi. Dobbiamo diagnosticarli, correggerli e produrre un report tecnico.

Il metodo da usare è sempre lo stesso:

```text
sintomo -> ipotesi -> verifica -> interpretazione -> correzione -> evidenza
```

---

## Obiettivi del laboratorio autonomo

Alla fine dell'attività dobbiamo produrre:

- `docs/report_autonomo_ud02.md`;
- `evidence/evidence_ud02_autonomo.md`;
- eventuali output significativi riportati nel report;
- commit e push sul repository remoto.

Il report deve contenere tre scenari:

1. script non eseguibile;
2. processo non responsivo a `SIGTERM`;
3. porta occupata.

---

## Regole operative

Durante l'attività:

- lavoriamo solo nella cartella della UD02;
- non usiamo `sudo` se non richiesto dal docente;
- non cancelliamo l'intera cartella di lavoro per risolvere un errore;
- non usiamo comandi troppo generici se possiamo usare un PID specifico;
- documentiamo sempre output prima e dopo la correzione;
- controlliamo `git status` prima del commit.

---

## 1. Preparazione ambiente autonomo

Posizioniamoci nella cartella della UD02:

```bash
cd ~/corso_obs/NOME-REPOSITORY/OBS_UD02_Permessi_Processi_Troubleshooting
pwd
```

Creiamo l'ambiente autonomo:

```bash
mkdir -p logs/autonomo/{bin,data,tmp,www}
mkdir -p docs evidence
```

Creiamo il report autonomo:

```bash
cat > docs/report_autonomo_ud02.md << 'EOF'
# Report autonomo UD02

## Scenario 1 - Script non eseguibile

### Sintomo

### Ipotesi

### Verifica

### Correzione

### Verifica finale

### Interpretazione

## Scenario 2 - Processo non responsivo

### Sintomo

### Ipotesi

### Verifica

### Correzione

### Verifica finale

### Interpretazione

## Scenario 3 - Porta occupata

### Sintomo

### Ipotesi

### Verifica

### Correzione

### Verifica finale

### Interpretazione

EOF
```

---

## 2. Scenario 1 - Script non eseguibile

Creiamo uno script intenzionalmente non eseguibile:

```bash
cat > logs/autonomo/bin/check_env.sh << 'EOF'
#!/usr/bin/env bash
echo "Ambiente UD02 operativo"
echo "Utente: $(whoami)"
echo "Directory: $(pwd)"
EOF

chmod 644 logs/autonomo/bin/check_env.sh
```

Proviamo a eseguirlo:

```bash
./logs/autonomo/bin/check_env.sh || true
```

Dobbiamo diagnosticare il problema.

Comandi consigliati:

```bash
ls -l logs/autonomo/bin/check_env.sh
head -n 1 logs/autonomo/bin/check_env.sh
stat logs/autonomo/bin/check_env.sh | head
```

Correggiamo solo il necessario:

```bash
chmod u+x logs/autonomo/bin/check_env.sh
./logs/autonomo/bin/check_env.sh
```

Aggiorniamo il report con:

- errore osservato;
- output di `ls -l` prima della correzione;
- comando di correzione;
- output finale dello script.

---

## 3. Scenario 2 - Processo non responsivo a SIGTERM

Creiamo un processo dimostrativo che intercetta `SIGTERM`.

```bash
cat > logs/autonomo/bin/autonomo_ignore_term.sh << 'EOF'
#!/usr/bin/env bash
trap 'echo "SIGTERM ricevuto ma ignorato"' TERM
echo "Processo autonomo avviato con PID $$"
while true; do
  sleep 5
done
EOF

chmod 755 logs/autonomo/bin/autonomo_ignore_term.sh
```

Avviamolo in background:

```bash
./logs/autonomo/bin/autonomo_ignore_term.sh > logs/autonomo/tmp/autonomo_ignore_term.log 2>&1 &
AUTO_PID=$!
echo "$AUTO_PID"
sleep 1
```

Verifichiamo:

```bash
ps -p "$AUTO_PID" -o pid,ppid,comm,etime,%cpu,%mem
```

Proviamo a terminarlo con `SIGTERM`:

```bash
kill -15 "$AUTO_PID"
sleep 1
ps -p "$AUTO_PID" -o pid,ppid,comm,etime,%cpu,%mem || true
cat logs/autonomo/tmp/autonomo_ignore_term.log
```

Se il processo è ancora attivo, terminiamolo forzatamente:

```bash
kill -9 "$AUTO_PID"
sleep 1
ps -p "$AUTO_PID" || true
```

Aggiorniamo il report con:

- PID del processo;
- comando di verifica;
- effetto di `SIGTERM`;
- motivo dell'uso di `SIGKILL`;
- verifica finale.

---

## 4. Scenario 3 - Porta occupata

Creiamo una pagina semplice:

```bash
echo "UD02 server autonomo" > logs/autonomo/www/index.html
```

Avviamo un server HTTP sulla porta `18081`:

```bash
python3 -m http.server 18081 --directory logs/autonomo/www > logs/autonomo/tmp/http_18081.log 2>&1 &
PORT_PID=$!
sleep 1
echo "$PORT_PID"
```

Verifichiamo che risponda:

```bash
curl -I http://localhost:18081 | head -n 1
```

Proviamo ad avviare un secondo server sulla stessa porta:

```bash
python3 -m http.server 18081 --directory logs/autonomo/www || true
```

Dobbiamo diagnosticare quale processo occupa la porta.

Su Linux:

```bash
ss -ltnp | grep 18081 || true
```

Su macOS:

```bash
lsof -iTCP:18081 -sTCP:LISTEN || true
```

Terminiamo solo il processo corretto:

```bash
kill -15 "$PORT_PID"
sleep 1
ps -p "$PORT_PID" || true
```

Verifichiamo che la porta non sia più in ascolto.

Su Linux:

```bash
ss -ltnp | grep 18081 || true
```

Su macOS:

```bash
lsof -iTCP:18081 -sTCP:LISTEN || true
```

Aggiorniamo il report con:

- sintomo `Address already in use`;
- comando usato per trovare il processo;
- PID individuato;
- comando di terminazione;
- verifica finale.

---

## 5. Evidenza autonoma

Creiamo l'evidenza finale:

```bash
cat > evidence/evidence_ud02_autonomo.md << 'EOF'
# Evidence autonoma UD02

## File prodotti

- `docs/report_autonomo_ud02.md`
- `evidence/evidence_ud02_autonomo.md`

## Scenari affrontati

- Script non eseguibile.
- Processo non responsivo a `SIGTERM`.
- Porta occupata.

## Metodo utilizzato

Per ogni scenario abbiamo seguito la sequenza:

sintomo -> ipotesi -> verifica -> interpretazione -> correzione -> evidenza

## Verifica finale

Il report autonomo contiene output e interpretazione per tutti e tre gli scenari.
EOF
```

---

## 6. Verifica minima

Eseguiamo lo script di verifica, se presente:

```bash
chmod 755 src/verifica_ud02.sh
./src/verifica_ud02.sh
```

Se lo script segnala file mancanti, completiamo prima la documentazione.

---

## 7. Commit e push

Controlliamo lo stato:

```bash
git status
```

Aggiungiamo i file richiesti:

```bash
git add docs/report_autonomo_ud02.md evidence/evidence_ud02_autonomo.md
```

Se abbiamo aggiornato anche script in `src/`, aggiungiamoli:

```bash
git add src/
```

Commit:

```bash
git commit -m "[OBS-UD02] Laboratorio autonomo diagnostica locale"
```

Push:

```bash
git push
```

---

## Domande finali

Rispondiamo brevemente nel report o durante il confronto finale:

1. Quale differenza c'è tra errore di permesso sul file ed errore di permesso sulla directory?
2. Perché un processo può restare attivo dopo `SIGTERM`?
3. Perché `SIGKILL` non dovrebbe essere la prima scelta?
4. Come possiamo dimostrare che una porta era occupata?
5. Quali evidenze sono davvero utili in un troubleshooting?

# OBS_UD01 - Laboratorio guidato

## Linux filesystem, file di testo, redirection, pipe e primo report tecnico

In questo laboratorio lavoriamo con la shell Linux per costruire un flusso operativo completo:

```text
cartelle -> file -> comandi -> filtri -> report -> evidenza -> commit
```

Il laboratorio riprende e fonde i contenuti dei precedenti LAB01 e LAB02, ma li organizza come una giornata unica orientata all’Observability.

---

## Scenario

Dobbiamo preparare una piccola area di lavoro per analizzare un log HTTP didattico. Il risultato finale sarà un report Markdown contenente:

- struttura dei file creata;
- comandi principali usati;
- conteggio delle richieste;
- conteggio degli errori;
- endpoint più richiesti;
- errori 5xx;
- breve interpretazione tecnica.

---

## Prerequisiti

Usiamo il terminale Ubuntu in WSL oppure una shell Linux/macOS equivalente.

I comandi richiesti sono:

```bash
pwd ls mkdir touch cp mv rm cat less head tail grep wc sort uniq tee awk find
```

Verifichiamo rapidamente:

```bash
which pwd ls mkdir touch cp mv rm cat less head tail grep wc sort uniq tee awk find
```

Se in Ubuntu manca qualche pacchetto di base:

```bash
sudo apt update
sudo apt install -y coreutils grep gawk sed findutils
```

---

## 1. Preparazione cartella UD01

Entriamo nel repository del corso.

```bash
cd ~/corso_obs/NOME-REPOSITORY
pwd
ls -la
```

Creiamo la cartella della UD01 secondo il nuovo standard.

```bash
mkdir -p labs/ud01/{docs,src,config,logs/work,evidence}
cd labs/ud01
pwd
find . -maxdepth 2 -type d | sort
```

📌 **Nota**

Nel repo storico i contenuti erano separati tra `lab01` e `lab02`. Nella nuova edizione li lavoriamo come una sola UD, quindi usiamo `labs/ud01`.

---

## 2. Orientamento nel filesystem

Eseguiamo alcuni comandi di orientamento.

```bash
pwd
ls
ls -la
```

Salviamo uno snapshot della cartella corrente.

```bash
ls -la > evidence/snapshot_iniziale.txt
cat evidence/snapshot_iniziale.txt
```

🔎 **Verifica**

Il file `evidence/snapshot_iniziale.txt` deve contenere l’elenco dei file e delle cartelle presenti in `labs/ud01`.

---

## 3. Creazione struttura di lavoro

Creiamo una struttura sotto `logs/work/course`.

```bash
mkdir -p logs/work/course/{lab,projects,datasets,scripts,reports}
find logs/work/course -maxdepth 2 -type d | sort
```

Salviamo l’elenco nel report parziale.

```bash
echo "# Report guidato UD01" > docs/report_guidato_ud01.md
echo "" >> docs/report_guidato_ud01.md
echo "## Struttura directory creata" >> docs/report_guidato_ud01.md
find logs/work/course -maxdepth 2 -type d | sort >> docs/report_guidato_ud01.md
```

Controlliamo il report.

```bash
cat docs/report_guidato_ud01.md
```

---

## 4. Operazioni su file

Entriamo nella cartella di lavoro del laboratorio.

```bash
cd logs/work/course/lab
```

Creiamo cinque file.

```bash
for i in {1..5}; do echo "file $i generato nel laboratorio guidato" > file$i.txt; done
ls -la
```

Copiamo due file nella cartella dei report.

```bash
cp file1.txt file2.txt ../reports/
ls -la ../reports
```

Rinominiamo un file.

```bash
mv file3.txt renamed3.txt
ls -la
```

Spostiamo un file nella cartella script.

```bash
mv file4.txt ../scripts/
ls -la ../scripts
```

Torniamo alla radice della UD01.

```bash
cd ~/corso_obs/NOME-REPOSITORY/labs/ud01
```

Aggiungiamo al report l’elenco dei file `.txt` trovati.

```bash
echo "" >> docs/report_guidato_ud01.md
echo "## File di testo presenti nel workspace" >> docs/report_guidato_ud01.md
find logs/work/course -type f -name "*.txt" | sort >> docs/report_guidato_ud01.md
```

---

## 5. Ricerca con `find`

Cerchiamo tutti i file sotto `logs/work/course`.

```bash
find logs/work/course -type f | sort
```

Creiamo un file binario di circa 2 KB.

```bash
head -c 2048 /dev/urandom > logs/work/course/lab/big.bin
```

Cerchiamo file più grandi di 1 KB.

```bash
find logs/work/course -type f -size +1k
```

Salviamo anche questo nel report.

```bash
echo "" >> docs/report_guidato_ud01.md
echo "## File maggiori di 1 KB" >> docs/report_guidato_ud01.md
find logs/work/course -type f -size +1k >> docs/report_guidato_ud01.md
```

---

## 6. Creazione dataset log HTTP

Creiamo un file log didattico.

```bash
cat > logs/work/raw_access.log << 'EOF'
2026-06-17T09:01:02Z GET / 200 34ms
2026-06-17T09:01:03Z GET /health 200 12ms
2026-06-17T09:01:06Z GET /login 200 55ms
2026-06-17T09:01:08Z POST /login 401 71ms
2026-06-17T09:01:11Z GET /api/users 500 840ms
2026-06-17T09:01:12Z GET /api/users 500 910ms
2026-06-17T09:01:13Z GET /api/users 200 120ms
2026-06-17T09:01:14Z GET /api/orders 200 160ms
2026-06-17T09:01:16Z GET /api/orders 200 170ms
2026-06-17T09:01:18Z GET /api/orders 503 1250ms
2026-06-17T09:01:22Z GET /docs 200 48ms
2026-06-17T09:01:25Z GET /docs 404 66ms
EOF
```

Verifichiamo il numero di righe.

```bash
wc -l logs/work/raw_access.log
head -n 5 logs/work/raw_access.log
tail -n 3 logs/work/raw_access.log
```

🔎 **Verifica**

Il file deve contenere 12 righe.

---

## 7. Lettura e filtri base

Visualizziamo tutto il file.

```bash
cat logs/work/raw_access.log
```

Usiamo `less` per leggere il file in modalità navigabile.

```bash
less logs/work/raw_access.log
```

Per uscire da `less`, premiamo `q`.

Estraiamo gli endpoint, che nel nostro formato sono il terzo campo.

```bash
awk '{print $3}' logs/work/raw_access.log
```

---

## 8. Errori HTTP con `grep`

Estraiamo gli errori 4xx e 5xx.

```bash
grep -E ' (4|5)[0-9]{2} ' logs/work/raw_access.log > logs/work/errors.log
cat logs/work/errors.log
wc -l logs/work/errors.log
```

Aggiungiamo il conteggio al report.

```bash
echo "" >> docs/report_guidato_ud01.md
echo "## Conteggio errori HTTP" >> docs/report_guidato_ud01.md
echo "Totale errori 4xx/5xx: $(wc -l < logs/work/errors.log)" >> docs/report_guidato_ud01.md
```

---

## 9. Classifica endpoint con pipe

Costruiamo la classifica degli endpoint più richiesti.

```bash
awk '{print $3}' logs/work/raw_access.log | sort | uniq -c | sort -nr > logs/work/top_endpoints.txt
cat logs/work/top_endpoints.txt
```

Aggiungiamo la classifica al report.

```bash
echo "" >> docs/report_guidato_ud01.md
echo "## Top endpoint" >> docs/report_guidato_ud01.md
cat logs/work/top_endpoints.txt >> docs/report_guidato_ud01.md
```

📌 **Nota**

La sequenza `sort | uniq -c` funziona correttamente perché `uniq` conta righe uguali consecutive. Per questo motivo prima ordiniamo.

---

## 10. Errori 5xx con `tee`

Isoliamo gli errori server 5xx e li salviamo in un file mostrando anche l’output a terminale.

```bash
grep -E ' 5[0-9]{2} ' logs/work/raw_access.log | tee logs/work/only_5xx.log
```

Aggiungiamo al report.

```bash
echo "" >> docs/report_guidato_ud01.md
echo "## Errori 5xx" >> docs/report_guidato_ud01.md
cat logs/work/only_5xx.log >> docs/report_guidato_ud01.md
```

---

## 11. Richieste lente

Nel nostro dataset la durata è il quinto campo, per esempio `1250ms`.

Estraiamo le richieste con durata maggiore o uguale a 800 ms.

```bash
awk '{duration=$5; gsub("ms", "", duration); if (duration + 0 >= 800) print $0}' logs/work/raw_access.log > logs/work/slow_requests.log
cat logs/work/slow_requests.log
```

Aggiungiamo al report.

```bash
echo "" >> docs/report_guidato_ud01.md
echo "## Richieste lente >= 800ms" >> docs/report_guidato_ud01.md
cat logs/work/slow_requests.log >> docs/report_guidato_ud01.md
```

---

## 12. Interpretazione tecnica minima

Completiamo il report con una breve interpretazione.

```bash
cat >> docs/report_guidato_ud01.md << 'EOF'

## Interpretazione tecnica

Il dataset contiene richieste HTTP verso endpoint diversi. Sono presenti errori client e server. Gli errori 5xx indicano problemi lato servizio o infrastruttura applicativa, mentre gli errori 4xx indicano richieste non valide, non autorizzate o risorse non trovate.

La presenza di richieste lente sugli stessi endpoint che generano errori può indicare un possibile degrado applicativo da analizzare nelle UD successive.
EOF
```

Leggiamo il report finale.

```bash
cat docs/report_guidato_ud01.md
```

---

## 13. Creazione evidenza finale

Creiamo un file di evidenza sintetico.

```bash
cat > evidence/evidence_ud01_guidato.md << 'EOF'
# Evidence UD01 - Laboratorio guidato

## Comandi principali utilizzati

- pwd
- ls -la
- mkdir -p
- find
- cp
- mv
- cat
- grep
- awk
- wc
- sort
- uniq
- tee

## File prodotti

- docs/report_guidato_ud01.md
- logs/work/raw_access.log
- logs/work/errors.log
- logs/work/top_endpoints.txt
- logs/work/only_5xx.log
- logs/work/slow_requests.log

## Verifica finale

Il report guidato è stato creato e contiene struttura directory, file di testo, errori HTTP, top endpoint, errori 5xx, richieste lente e interpretazione tecnica.

## Problemi incontrati

Nessun problema.
EOF
```

Verifichiamo che i file principali esistano.

```bash
test -s docs/report_guidato_ud01.md && echo "REPORT GUIDATO OK"
test -s evidence/evidence_ud01_guidato.md && echo "EVIDENCE GUIDATO OK"
```

---

## 14. Commit e push

Torniamo alla radice del repository.

```bash
cd ~/corso_obs/NOME-REPOSITORY
git status
```

Aggiungiamo i file prodotti. I file dentro `logs/` possono essere ignorati se il repository li esclude con `.gitignore`; l’evidenza e il report devono invece essere versionati.

```bash
git add labs/ud01/docs/report_guidato_ud01.md labs/ud01/evidence/evidence_ud01_guidato.md
git commit -m "[UD01] Laboratorio guidato Linux file e log"
git push
```

---

## Criteri di completamento

Il laboratorio guidato è completato quando:

- la cartella `labs/ud01` è stata creata;
- il report `docs/report_guidato_ud01.md` è presente;
- l’evidenza `evidence/evidence_ud01_guidato.md` è presente;
- i comandi su file, redirection, pipe e filtri sono stati eseguiti;
- il commit è visibile sul repository remoto.

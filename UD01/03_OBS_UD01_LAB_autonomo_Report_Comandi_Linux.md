# OBS_UD01 - Laboratorio autonomo

## Report tecnico da log HTTP usando comandi Linux

## Scenario

Nel laboratorio guidato abbiamo creato un piccolo dataset log e prodotto un report assistito.

Nel laboratorio autonomo lavoriamo su un nuovo dataset. L’obiettivo è produrre un report tecnico senza ripetere meccanicamente gli stessi comandi, ma applicando il metodo:

```text
osservare -> filtrare -> contare -> classificare -> interpretare -> documentare
```

---

## Briefing docente per l’avvio del pomeriggio

Il docente presenta lo scenario e chiarisce che il risultato atteso non è solo una lista di comandi. Il report deve contenere dati e interpretazione minima.

Il lavoro può essere svolto individualmente o in coppia. Ogni partecipante deve comunque consegnare il proprio report nel repository.

---

## Obiettivi del laboratorio autonomo

Al termine dell’attività dobbiamo produrre:

- un dataset `logs/work/web_access_autonomo.log`;
- un report `docs/report_autonomo_ud01.md`;
- un’evidenza `evidence/evidence_ud01_autonomo.md`;
- un commit e push sul repository remoto.

Il report deve rispondere a queste domande:

1. quante richieste totali contiene il log;
2. quanti errori 4xx sono presenti;
3. quanti errori 5xx sono presenti;
4. quali sono i tre endpoint più richiesti;
5. quali richieste hanno durata maggiore o uguale a 1000 ms;
6. quali status code compaiono e quante volte;
7. quale possibile problema operativo emerge dal dataset.

---

## 1. Preparazione workspace

Posizioniamoci nella cartella della UD01.

```bash
cd ~/corso_obs/NOME-REPOSITORY/labs/ud01
pwd
mkdir -p logs/work docs evidence
```

---

## 2. Creazione dataset autonomo

Creiamo il file `web_access_autonomo.log`.

```bash
cat > logs/work/web_access_autonomo.log << 'EOF'
2026-06-17T14:00:01Z GET / 200 31ms
2026-06-17T14:00:03Z GET /health 200 10ms
2026-06-17T14:00:05Z GET /api/products 200 115ms
2026-06-17T14:00:07Z GET /api/products 200 118ms
2026-06-17T14:00:09Z GET /api/products 500 980ms
2026-06-17T14:00:11Z GET /api/products 500 1100ms
2026-06-17T14:00:13Z GET /api/cart 200 180ms
2026-06-17T14:00:15Z POST /api/cart 201 240ms
2026-06-17T14:00:17Z POST /api/cart 503 1450ms
2026-06-17T14:00:20Z GET /api/orders 200 210ms
2026-06-17T14:00:22Z GET /api/orders 200 230ms
2026-06-17T14:00:24Z GET /api/orders 504 1800ms
2026-06-17T14:00:27Z GET /login 200 60ms
2026-06-17T14:00:29Z POST /login 401 75ms
2026-06-17T14:00:31Z POST /login 401 80ms
2026-06-17T14:00:33Z GET /admin 403 50ms
2026-06-17T14:00:35Z GET /docs 200 45ms
2026-06-17T14:00:37Z GET /docs 404 65ms
2026-06-17T14:00:39Z GET /docs 200 47ms
2026-06-17T14:00:42Z GET /metrics 200 20ms
2026-06-17T14:00:44Z GET /metrics 200 19ms
2026-06-17T14:00:46Z GET /api/products 200 125ms
2026-06-17T14:00:49Z GET /api/orders 500 1320ms
2026-06-17T14:00:52Z GET /api/orders 200 260ms
EOF
```

Verifichiamo il numero di righe.

```bash
wc -l logs/work/web_access_autonomo.log
```

Il risultato atteso è 24 righe.

---

## 3. Creazione report

Creiamo il file report.

```bash
echo "# Report autonomo UD01" > docs/report_autonomo_ud01.md
echo "" >> docs/report_autonomo_ud01.md
echo "## Dataset" >> docs/report_autonomo_ud01.md
echo "File analizzato: logs/work/web_access_autonomo.log" >> docs/report_autonomo_ud01.md
```

---

## 4. Attività richieste

Completare il report aggiungendo le sezioni seguenti.

### 4.1 Richieste totali

Aggiungere al report il numero totale di righe del dataset.

Suggerimento:

```bash
wc -l < logs/work/web_access_autonomo.log
```

### 4.2 Errori 4xx

Aggiungere al report il numero di errori 4xx.

Suggerimento:

```bash
grep -E ' 4[0-9]{2} ' logs/work/web_access_autonomo.log
```

### 4.3 Errori 5xx

Aggiungere al report il numero di errori 5xx.

Suggerimento:

```bash
grep -E ' 5[0-9]{2} ' logs/work/web_access_autonomo.log
```

### 4.4 Top 3 endpoint

Aggiungere al report i tre endpoint più richiesti.

Suggerimento:

```bash
awk '{print $3}' logs/work/web_access_autonomo.log | sort | uniq -c | sort -nr | head -n 3
```

### 4.5 Richieste lente

Aggiungere al report le richieste con durata maggiore o uguale a 1000 ms.

Suggerimento:

```bash
awk '{duration=$5; gsub("ms", "", duration); if (duration + 0 >= 1000) print $0}' logs/work/web_access_autonomo.log
```

### 4.6 Distribuzione status code

Aggiungere al report quanti status code di ogni tipo sono presenti.

Suggerimento:

```bash
awk '{print $4}' logs/work/web_access_autonomo.log | sort | uniq -c | sort -nr
```

### 4.7 Interpretazione

Aggiungere una sezione finale con massimo 8-10 righe.

La sezione deve rispondere a queste domande:

- quale endpoint sembra più problematico;
- se il problema appare più collegato a errori client o server;
- se le richieste lente sono isolate o concentrate su endpoint specifici;
- quale controllo sarebbe utile fare nella UD successiva.

---

## 5. Evidenza finale

Creare il file:

```bash
evidence/evidence_ud01_autonomo.md
```

Contenuto minimo richiesto:

```md
# Evidence UD01 - Laboratorio autonomo

## File consegnati

- docs/report_autonomo_ud01.md

## Verifiche eseguite

- conteggio richieste totali;
- conteggio errori 4xx;
- conteggio errori 5xx;
- top endpoint;
- richieste lente;
- distribuzione status code;
- interpretazione tecnica.

## Problemi incontrati

Scrivere eventuali problemi oppure "Nessun problema".
```

---

## 6. Verifica locale

Eseguire:

```bash
test -s docs/report_autonomo_ud01.md && echo "REPORT AUTONOMO OK"
test -s evidence/evidence_ud01_autonomo.md && echo "EVIDENCE AUTONOMO OK"
```

Se è disponibile lo script di verifica fornito nella cartella `src`, è possibile copiarlo nel repository ed eseguirlo dalla cartella `labs/ud01`:

```bash
bash src/verifica_ud01.sh
```

---

## 7. Commit e push

Dalla radice del repository:

```bash
cd ~/corso_obs/NOME-REPOSITORY
git status
git add labs/ud01/docs/report_autonomo_ud01.md labs/ud01/evidence/evidence_ud01_autonomo.md
git commit -m "[UD01] Laboratorio autonomo analisi log Linux"
git push
```

---

## Criteri di completamento

Il laboratorio autonomo è completato quando:

- `docs/report_autonomo_ud01.md` contiene tutte le sezioni richieste;
- `evidence/evidence_ud01_autonomo.md` è presente;
- il report contiene almeno una interpretazione tecnica e non solo output di comandi;
- commit e push sono stati eseguiti;
- il repository remoto mostra i file consegnati.

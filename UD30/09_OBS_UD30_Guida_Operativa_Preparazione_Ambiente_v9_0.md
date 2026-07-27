# Guida operativa — Preparazione dell’ambiente UD30

## Scopo

Questa preparazione deve essere completata prima della lezione. Il download dei modelli durante il laboratorio consumerebbe tempo e banda e renderebbe difficile distinguere problemi di installazione da problemi didattici.

## Configurazione raccomandata per l’Academy

Poiché il corso usa WSL e Python in Linux, la configurazione più lineare è eseguire anche Ollama nello stesso ambiente WSL.

```text
VS Code Remote WSL
Python in WSL
client ollama in WSL
servizio Ollama in WSL
modello locale
```

È possibile usare Ollama installato su Windows, ma il collegamento tra Python in WSL e il servizio Windows dipende dalla configurazione di rete. Questa variante non è il percorso principale del materiale.

---

## 1. Verificare Python

```bash
python3 --version
```

Versione consigliata: Python 3.10 o successiva.

---

## 2. Creare l’ambiente virtuale

Dalla cartella `UD30`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verificare:

```bash
python -c "import ollama, pandas; print('dipendenze OK')"
```

La cartella `.venv` non deve essere versionata in Git.

---

## 3. Installare e avviare Ollama

Per Linux/WSL seguire la documentazione ufficiale. Il comando corrente indicato da Ollama è:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Se il servizio systemd è disponibile:

```bash
sudo systemctl start ollama
sudo systemctl status ollama
```

Se systemd non è disponibile, avviare manualmente in un terminale dedicato:

```bash
ollama serve
```

Lasciare il terminale aperto.

Verificare:

```bash
ollama --version
ollama list
```

---

## 4. Scaricare i modelli prima della lezione

Obbligatorio:

```bash
ollama pull llama3.2:1b
```

Fallback leggero:

```bash
ollama pull gemma3:1b
```

Fallback estremo, da scaricare solo dove necessario:

```bash
ollama pull gemma3:270m
```

Solo sui PC adeguati:

```bash
ollama pull llama3.2:3b
```

Controllare:

```bash
ollama list
```

---

## 5. Test manuale

```bash
ollama run llama3.2:1b
```

Prompt:

```text
Rispondi con una sola frase: che cosa significa osservabilità?
```

Uscire con:

```text
/bye
```

---

## 6. Test Python

```bash
python3 scripts/00_check_ollama.py
```

Esito atteso:

```text
[OK] package Python disponibile
[OK] servizio Ollama raggiungibile
[OK] modello configurato disponibile
[OK] richiesta completata
```

---

## 7. Scelta in base al PC

### Percorso A

`llama3.2:1b` risponde in tempo accettabile: usare il modello di riferimento.

### Percorso B

Il modello è troppo lento o non entra in memoria: usare:

```bash
export OLLAMA_MODEL=gemma3:1b
```

### Percorso C

Anche il modello da 1B non è utilizzabile: usare `gemma3:270m` esclusivamente per la chiamata Python e la telemetria. Per l’analisi qualitativa usare le risposte predisposte.

```bash
export OLLAMA_MODEL=gemma3:270m
```

### Percorso D

Nessun modello locale è utilizzabile: usare i file in `fallback`.

Il partecipante potrà comunque:

- confrontare le risposte;
- compilare la matrice claim–evidence;
- analizzare la telemetria;
- completare l’handoff.

---

## 8. Problemi frequenti

### `Connection refused`

Ollama non è avviato oppure l’host configurato non è raggiungibile.

```bash
ollama serve
```

### `model not found`

```bash
ollama pull llama3.2:1b
```

### Python non trova `ollama`

Attivare `.venv` e installare:

```bash
pip install -r requirements.txt
```

### Prima chiamata molto lenta

Il modello può dover essere caricato. Confrontare `load_ms` tra prima e seconda richiesta.

### Memoria insufficiente

Passare al fallback leggero oppure usare gli output predisposti.

---

## 9. Variabili d’ambiente

```bash
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=llama3.2:1b
```

Per il confronto:

```bash
export OLLAMA_MODELS=llama3.2:1b,llama3.2:3b
```

---

## 10. Checklist docente

- [ ] tutti i PC hanno Python;
- [ ] `.venv` creata;
- [ ] dipendenze installate;
- [ ] Ollama avviato;
- [ ] `llama3.2:1b` scaricato;
- [ ] `gemma3:1b` disponibile sui PC che richiedono il fallback;
- [ ] `gemma3:270m` o file predisposti disponibili per i casi estremi;
- [ ] test Python riuscito;
- [ ] evidence packet verificato;
- [ ] account cloud non obbligatori per ogni partecipante;
- [ ] dati del laboratorio interamente sintetici.

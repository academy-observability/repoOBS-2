# Preflight operativo — Compatibilità e prima chat Ollama da WSL

## Scopo

Questo file completa la guida di preparazione dell’ambiente con una procedura unica per:

- distinguere **Ollama** dalla sua modalità chat;
- installare Ollama quando non è presente;
- verificare un’installazione già esistente;
- controllare Python e le librerie usate dagli script;
- avviare il servizio Ollama in WSL;
- verificare i modelli locali;
- eseguire una breve conversazione di prova nel terminale;
- confermare, con una chiamata reale, che l’ambiente sia idoneo ai laboratori.

> Questa procedura deve essere completata **prima del LAB 04**. Il download dei modelli non deve essere lasciato all’inizio del laboratorio.

---

## 1. Che cosa significa “Ollama Chat” nella UD30

**Ollama Chat non è un secondo prodotto da installare.**

Nel percorso WSL della UD30 vengono utilizzati:

```text
Ollama             runtime locale che esegue il modello
ollama serve       servizio locale Ollama
ollama run MODELLO sessione di chat interattiva nel terminale
package ollama     client Python usato dagli script
```

La chat si svolge quindi nel terminale WSL:

```bash
ollama run llama3.2:1b
```

Dopo il caricamento del modello compare il prompt interattivo:

```text
>>>
```

Il partecipante scrive o incolla il messaggio dopo `>>>`. Non sono necessari una finestra grafica, un browser o un’applicazione denominata “Ollama Chat”.

---

## 2. Architettura prevista

La configurazione raccomandata mantiene tutti i componenti nello stesso ambiente Linux:

```text
┌─────────────────────────────────────┐
│ WSL Linux                           │
│                                     │
│ VS Code Remote WSL                  │
│        │                            │
│        ├── Python + .venv           │
│        │       │                    │
│        │       └── package ollama   │
│        │                    │       │
│ terminale ── ollama run     │       │
│                    │        │       │
│              Ollama API locale      │
│          http://localhost:11434     │
│                    │                │
│               modello locale       │
└─────────────────────────────────────┘
```

Installare Ollama in Windows e usare Python in WSL è possibile, ma introduce una dipendenza dalla configurazione di rete fra Windows e WSL. **Non è il percorso principale della UD30.**

---

## 3. Posizionarsi nella cartella corretta

Aprire VS Code collegato a WSL oppure un terminale WSL e raggiungere la cartella `UD30`:

```bash
cd /percorso/della/UD30
pwd
```

Controllare che siano presenti almeno:

```bash
ls
```

```text
requirements.txt
scripts
prompts
evidence
```

---

## 4. Verificare Python e l’ambiente virtuale

### 4.1 Controllo della versione

```bash
python3 --version
```

Requisito della UD30:

```text
Python 3.10 o successivo
```

Il client Python ufficiale di Ollama supporta anche versioni precedenti, ma la UD30 adotta Python 3.10 come baseline didattica comune.

### 4.2 Creazione o riutilizzo della `.venv`

Se la cartella `.venv` non esiste:

```bash
python3 -m venv .venv
```

Attivarla:

```bash
source .venv/bin/activate
```

Il prompt del terminale dovrebbe mostrare `(.venv)`.

Verificare che `python` e `pip` appartengano alla `.venv`:

```bash
which python
which pip
```

I percorsi devono contenere:

```text
.venv/bin/python
.venv/bin/pip
```

---

## 5. Installare e verificare le librerie Python

Installare o aggiornare le dipendenze dichiarate dalla UD:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Controllare che non vi siano dipendenze incompatibili:

```bash
python -m pip check
```

Esito atteso:

```text
No broken requirements found.
```

Visualizzare le versioni effettive:

```bash
python - <<'PY'
import sys
from importlib.metadata import version

import pandas

print(f"Python:         {sys.version.split()[0]}")
print(f"pandas:         {pandas.__version__}")
print(f"client ollama:  {version('ollama')}")

if sys.version_info < (3, 10):
    raise SystemExit("[ERRORE] La UD30 richiede Python 3.10 o successivo")

major, minor = (int(x) for x in pandas.__version__.split('.')[:2])
if (major, minor) < (2, 0):
    raise SystemExit("[ERRORE] La UD30 richiede pandas 2.0 o successivo")

print("[OK] Versioni Python e pandas compatibili con la UD30")
PY
```

### Criterio di compatibilità del client Python

Per il package `ollama` non viene fissato in questa UD un numero minimo arbitrario. La compatibilità viene confermata in modo più affidabile quando il client riesce a:

1. collegarsi al servizio;
2. leggere l’elenco dei modelli;
3. eseguire `client.chat()`;
4. restituire la risposta e i metadati usati dagli script.

Questi controlli saranno svolti dallo script `scripts/00_check_ollama.py`.

---

## 6. Verificare se Ollama è già installato

```bash
command -v ollama
ollama --version
```

### Caso A — comando trovato

L’installazione esiste. Proseguire con il controllo del servizio e della release.

### Caso B — `ollama: command not found`

Installare Ollama in WSL usando il metodo ufficiale per Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Chiudere e riaprire il terminale solo se il comando non viene immediatamente trovato nel `PATH`.

---

## 7. Verificare o aggiornare la release di Ollama

La UD30 utilizza anche modelli `gemma3`. La famiglia Gemma 3 richiede:

```text
Ollama 0.6.0 o successivo
```

La scelta più semplice per l’aula è utilizzare una release stabile corrente, non una pre-release.

### 7.1 Controllo tramite CLI

```bash
ollama --version
```

### 7.2 Controllo tramite API locale

Il controllo API verifica la release del **servizio realmente raggiunto**, non soltanto quella del comando presente nel `PATH`:

```bash
curl http://localhost:11434/api/version
```

Esempio di risposta:

```json
{"version":"0.x.y"}
```

### 7.3 Verifica automatica della versione minima

Eseguire quando il servizio è già attivo:

```bash
python - <<'PY'
import json
import re
import urllib.request

MINIMUM = (0, 6, 0)
URL = "http://localhost:11434/api/version"


def as_tuple(text: str) -> tuple[int, int, int]:
    values = [int(x) for x in re.findall(r"\d+", text)[:3]]
    values += [0] * (3 - len(values))
    return tuple(values[:3])


try:
    with urllib.request.urlopen(URL, timeout=3) as response:
        current_text = json.load(response)["version"]
except Exception as exc:
    raise SystemExit(f"[ERRORE] Servizio Ollama non raggiungibile: {exc}")

current = as_tuple(current_text)
print(f"Versione servizio Ollama: {current_text}")

if current < MINIMUM:
    raise SystemExit(
        "[ERRORE] Release non idonea ai modelli Gemma 3: "
        "richiesta Ollama 0.6.0 o successiva"
    )

print("[OK] Release Ollama compatibile con i modelli previsti dalla UD30")
PY
```

### 7.4 Aggiornamento di un’installazione Linux esistente

Per aggiornare Ollama alla release stabile corrente, rieseguire lo script ufficiale:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Dopo l’aggiornamento:

```bash
ollama --version
```

> Non aggiornare contemporaneamente tutti i PC durante la lezione. Il docente deve verificare preventivamente la release su una macchina rappresentativa e distribuire una configurazione omogenea.

---

## 8. Avviare il servizio Ollama in WSL

### Percorso A — systemd disponibile

```bash
sudo systemctl start ollama
sudo systemctl status ollama
```

Lo stato atteso contiene:

```text
active (running)
```

Per uscire dalla schermata di stato premere `q`.

### Percorso B — systemd non disponibile

Aprire un primo terminale WSL ed eseguire:

```bash
ollama serve
```

Lasciare questo terminale aperto. Aprire un **secondo terminale WSL** per i comandi successivi.

### Verifica del servizio

```bash
curl http://localhost:11434/api/version
```

Se viene restituito un JSON con la versione, il servizio è raggiungibile.

---

## 9. Controllare i modelli disponibili

```bash
ollama list
```

Il modello di riferimento deve comparire con il tag completo:

```text
llama3.2:1b
```

Se manca:

```bash
ollama pull llama3.2:1b
```

Fallback previsti:

```bash
ollama pull gemma3:1b
ollama pull gemma3:270m
```

Solo sui PC adeguati:

```bash
ollama pull llama3.2:3b
```

### Attenzione ai tag

Usare il tag esatto indicato dalla UD. Ad esempio:

```bash
ollama run gemma3:1b
```

Non sostituirlo automaticamente con:

```bash
ollama run gemma3
```

Il tag generico può riferirsi a un modello più grande e richiedere molte più risorse.

---

## 10. Breve interazione di prova con la chat CLI

Avviare il modello di riferimento:

```bash
ollama run llama3.2:1b
```

Dopo la comparsa di `>>>`, eseguire questa breve conversazione.

### Primo messaggio — verifica della risposta

```text
Rispondi con una sola frase: che cosa significa osservabilità di un sistema software?
```

Verificare che il modello produca una risposta e restituisca il controllo al prompt `>>>`.

### Secondo messaggio — verifica del contesto conversazionale

```text
Ora indica, in due punti distinti, una metrica e un log che potrebbero aiutare a osservare un servizio lento.
```

Il modello deve comprendere che “ora” si collega al tema introdotto nel messaggio precedente. Questa prova mostra che la sessione conserva la cronologia della conversazione.

### Terzo messaggio — prima applicazione del principio didattico

```text
Fatti disponibili:
- la latenza p95 è salita da 200 ms a 1800 ms;
- il traffico è rimasto stabile;
- è stata rilasciata una nuova versione un'ora prima.

Distingui chiaramente:
1. fatti osservati;
2. ipotesi possibile;
3. verifica necessaria.
Non presentare la nuova release come causa certa.
```

### Che cosa osservare

Non è necessario ottenere una risposta identica a quella del docente. Verificare invece che:

- il modello risponda senza errori tecnici;
- distingua almeno in parte fatti e ipotesi;
- non trasformi automaticamente la correlazione temporale in causalità;
- proponga una verifica successiva;
- la velocità sia utilizzabile sul PC.

Per terminare la sessione:

```text
/bye
```

---

## 11. Preflight funzionale completo

Con la `.venv` attiva, dalla cartella `UD30`:

```bash
python3 scripts/00_check_ollama.py
```

Questo è il controllo decisivo perché verifica l’intera catena:

```text
Python
  ↓
package ollama
  ↓
API locale
  ↓
servizio Ollama
  ↓
modello configurato
  ↓
risposta reale
```

Esito atteso:

```text
[OK] package Python ollama disponibile
[OK] servizio Ollama raggiungibile
[OK] modello configurato disponibile
[OK] richiesta completata
```

Il solo comando `ollama --version` **non è sufficiente**: dimostra che la CLI esiste, ma non che il servizio, il modello e il client Python funzionino insieme.

---

## 12. Registrare l’ambiente effettivamente collaudato

Creare una fotografia testuale dell’ambiente:

```bash
mkdir -p runtime

{
  echo "=== DATA ==="
  date --iso-8601=seconds
  echo
  echo "=== SISTEMA ==="
  uname -a
  echo
  echo "=== PYTHON ==="
  python --version
  echo
  echo "=== PACKAGE ==="
  python -m pip show ollama pandas
  echo
  echo "=== PIP CHECK ==="
  python -m pip check
  echo
  echo "=== OLLAMA CLI ==="
  ollama --version
  echo
  echo "=== OLLAMA SERVER ==="
  curl -s http://localhost:11434/api/version
  echo
  echo
  echo "=== MODELLI ==="
  ollama list
} > runtime/preflight_environment.txt
```

Il file prodotto consente di ricostruire quale ambiente sia stato realmente utilizzato:

```text
runtime/preflight_environment.txt
```

Non contiene prompt o evidenze sensibili, ma prima di condividerlo è comunque opportuno verificarne il contenuto.

---

## 13. Matrice di idoneità

| Controllo | Idoneo | Non idoneo o da correggere |
|---|---|---|
| Python | 3.10 o successivo | versione precedente |
| pandas | 2.0 o successivo | versione precedente o import fallito |
| Client Python `ollama` | import, `list()` e `chat()` riusciti | errore di import o chiamata |
| Servizio Ollama | API `localhost:11434` raggiungibile | `Connection refused` o timeout |
| Release Ollama | 0.6.0 o successiva se si usa Gemma 3 | release precedente con modelli Gemma 3 |
| Modello | tag richiesto presente in `ollama list` | `model not found` |
| Chat CLI | risposta ottenuta e `/bye` funzionante | errore o blocco permanente |
| Preflight Python | tutti i messaggi `[OK]` | almeno un `[ERRORE]` |
| Prestazioni | latenza accettabile per la prova | usare modello più leggero o fallback |

---

## 14. Problemi frequenti

### La CLI esiste, ma il servizio non risponde

Sintomo:

```text
Connection refused
```

Correzione:

```bash
ollama serve
```

oppure:

```bash
sudo systemctl start ollama
```

### Il comando usato non è quello installato in WSL

Controllare:

```bash
which ollama
```

Il percorso deve appartenere all’ambiente Linux. Evitare di mescolare inconsapevolmente CLI Windows, servizio Windows e Python WSL.

### Il modello non è presente

```bash
ollama pull llama3.2:1b
```

### La chat è molto lenta alla prima richiesta

La prima chiamata può includere il caricamento del modello in memoria. Eseguire un secondo messaggio e confrontare i tempi. Una prima risposta lenta non indica necessariamente un errore.

### Il PC non dispone di memoria sufficiente

Provare nell’ordine:

```bash
ollama run gemma3:1b
ollama run gemma3:270m
```

`gemma3:270m` serve principalmente a completare la prova tecnica. Per il confronto qualitativo utilizzare i file predisposti nella cartella `fallback`.

### `pip check` segnala conflitti

Ricreare la `.venv` anziché modificare l’installazione globale:

```bash
deactivate 2>/dev/null || true
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

---

## 15. Checklist finale del partecipante

- [ ] sto lavorando nella cartella `UD30` dentro WSL;
- [ ] la `.venv` è attiva;
- [ ] Python è almeno 3.10;
- [ ] pandas è almeno 2.0;
- [ ] `python -m pip check` non segnala conflitti;
- [ ] `ollama --version` funziona;
- [ ] il servizio risponde su `http://localhost:11434`;
- [ ] la release è compatibile con i modelli scelti;
- [ ] `llama3.2:1b` oppure il fallback è presente;
- [ ] la breve chat da terminale è stata completata;
- [ ] sono uscito dalla chat con `/bye`;
- [ ] `python3 scripts/00_check_ollama.py` termina con successo;
- [ ] ho registrato l’ambiente in `runtime/preflight_environment.txt`.

---

## 16. Esito della preparazione

L’ambiente può essere considerato pronto soltanto quando sono verificate entrambe le condizioni:

```text
controlli di versione superati
+
chiamata reale al modello riuscita
```

In sintesi:

```text
CLI presente
≠ ambiente completo
```

```text
release recente
≠ integrazione funzionante
```

```text
preflight funzionale riuscito
= ambiente idoneo ai laboratori UD30
```

---

## Fonti tecniche ufficiali

- Installazione e aggiornamento Linux: <https://docs.ollama.com/linux>
- Riferimento CLI: <https://docs.ollama.com/cli>
- Endpoint di versione: <https://docs.ollama.com/api-reference/get-version>
- Client Python ufficiale: <https://github.com/ollama/ollama-python>
- Modelli Gemma 3 e requisito Ollama 0.6+: <https://ollama.com/library/gemma3>

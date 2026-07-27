# Preflight — Ollama Windows e client Python in WSL

## Scopo

Questo controllo conferma l'intera catena:

```text
Python WSL
  ↓
package ollama
  ↓
rete WSL → Windows
  ↓
API Ollama Windows
  ↓
modello locale
  ↓
risposta e telemetria
```

Completare prima il file `00A`.

## 1. Posizionarsi nella UD

```bash
cd /percorso/della/UD30
pwd
ls
```

## 2. Preparare la `.venv`

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

Esito atteso:

```text
No broken requirements found.
```

## 3. Configurare l'endpoint

Mirrored:

```bash
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
```

NAT:

```bash
export WINDOWS_HOST=$(ip route show | awk '/default/ {print $3; exit}')
export OLLAMA_BASE_URL="http://$WINDOWS_HOST:11434"
```

Modello:

```bash
export OLLAMA_MODEL="llama3.2:1b"
```

## 4. Verificare la CLI Windows da WSL

```bash
ollama.exe --version
ollama.exe list
```

Se il modello manca:

```bash
ollama.exe pull llama3.2:1b
```

Fallback:

```bash
ollama.exe pull gemma3:1b
```

## 5. Verificare l'API dal lato Linux

```bash
curl "$OLLAMA_BASE_URL/api/version"
curl "$OLLAMA_BASE_URL/api/tags"
```

Non usare `curl.exe` come unico test: gli script Python sono processi Linux.

## 6. Prima chat dal terminale WSL

```bash
ollama.exe run "$OLLAMA_MODEL"
```

Messaggio di prova:

```text
Rispondi con una frase: qual è la differenza tra un fatto osservato e un'ipotesi?
```

Poi:

```text
Fatti:
- p95 frontend 510 ms;
- chiamata backend 145 ms;
- non sono stati analizzati tutti i log.

Separa fatti, ipotesi e verifiche. Non inventare componenti.
```

Uscire con:

```text
/bye
```

## 7. Preflight Python

```bash
python3 scripts/00_check_ollama.py
```

Esito atteso:

```text
[OK] endpoint configurato
[OK] package Python ollama disponibile
[OK] API Ollama raggiungibile
[OK] modello disponibile
[OK] inferenza completata
```

## 8. Registrare l'ambiente

```bash
mkdir -p runtime

{
  echo "=== DATA ==="
  date --iso-8601=seconds
  echo
  echo "=== WSL ==="
  uname -a
  echo
  echo "=== PYTHON ==="
  python --version
  echo
  echo "=== PACKAGE ==="
  python -m pip show ollama pandas
  echo
  echo "=== ENDPOINT ==="
  echo "$OLLAMA_BASE_URL"
  echo
  echo "=== OLLAMA WINDOWS ==="
  ollama.exe --version
  echo
  echo "=== API ==="
  curl -s "$OLLAMA_BASE_URL/api/version"
  echo
  echo "=== MODELLI ==="
  ollama.exe list
} > runtime/preflight_environment.txt
```

## 9. Problemi frequenti

### `ollama.exe` funziona ma Python restituisce connection refused

La CLI Windows e Python WSL stanno usando percorsi diversi. Verificare `OLLAMA_BASE_URL` e il test con `curl` Linux.

### `curl.exe` funziona ma `curl` non funziona

Ollama è disponibile dal lato Windows, ma non dalla rete WSL. Completare mirrored o NAT.

### `model not found`

```bash
ollama.exe pull "$OLLAMA_MODEL"
```

### Prima risposta lenta

La prima inferenza può includere il caricamento del modello in memoria. Confrontare la seconda richiesta e osservare `load_duration`.

### Memoria insufficiente

```bash
export OLLAMA_MODEL="gemma3:1b"
```

`gemma3:270m` è ammesso soltanto per verificare il funzionamento tecnico della catena.

## Checklist

- [ ] Ollama Windows risponde in PowerShell;
- [ ] `ollama.exe` funziona da WSL;
- [ ] `curl` Linux raggiunge `$OLLAMA_BASE_URL`;
- [ ] il modello con tag esplicito è presente;
- [ ] la `.venv` è attiva;
- [ ] `pip check` non segnala conflitti;
- [ ] `scripts/00_check_ollama.py` termina con successo;
- [ ] `runtime/preflight_environment.txt` è stato prodotto.

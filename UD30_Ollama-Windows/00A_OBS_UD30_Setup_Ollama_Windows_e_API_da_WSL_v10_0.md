# Setup operativo — Ollama su Windows e accesso API da WSL

## Scopo

La configurazione della UD30 per Ollama installato su Windows è:

```text
Ollama e modelli → Windows
script e terminale → WSL Ubuntu
```

Questo file permette di:

- verificare Ollama in Windows;
- usare la CLI Windows dal terminale WSL;
- rendere l'API raggiungibile dagli script Python Linux;
- scegliere tra rete **mirrored** e fallback **NAT**;
- evitare una seconda installazione di Ollama in WSL.

---

## 1. Distinguere i due tipi di comando

Da WSL:

```bash
ollama.exe list
```

esegue il programma Windows tramite l'interoperabilità WSL.

Da WSL:

```bash
curl http://127.0.0.1:11434/api/tags
```

esegue invece `curl` Linux. Questo secondo comando verifica la stessa rete usata dagli script Python WSL.

La prova con `curl.exe` è utile, ma non sostituisce quella con `curl`:

```bash
curl.exe http://localhost:11434/api/tags
```

```text
curl.exe → lato Windows
curl     → lato Linux/WSL
```

---

## 2. Verificare Ollama in Windows

Aprire PowerShell:

```powershell
ollama --version
ollama list
curl.exe http://localhost:11434/api/version
curl.exe http://localhost:11434/api/tags
```

Se questi comandi falliscono, risolvere prima Ollama Windows:

1. avviare Ollama dal menu Start;
2. controllare l'icona nell'area di notifica;
3. ripetere i comandi;
4. verificare che la porta `11434` non sia occupata da un altro processo.

Da WSL deve funzionare anche:

```bash
ollama.exe --version
ollama.exe list
```

Se `ollama.exe` non viene trovato, verificare che l'interoperabilità Windows/WSL non sia stata disabilitata e che Ollama sia nel `PATH` di Windows.

---

## 3. Verificare WSL

Da PowerShell:

```powershell
wsl --version
wsl --status
wsl --list --verbose
```

La distribuzione usata deve risultare in versione `2`.

### Aggiornamento solo quando necessario

```powershell
wsl --update
```

Se il canale Microsoft Store non è raggiungibile:

```powershell
wsl --update --web-download
```

Se compare un errore di risoluzione del nome, verificare DNS, proxy, VPN o policy aziendali. L'errore di download non dimostra che Ollama sia guasto.

---

# Percorso principale — rete mirrored

## 4. Quando usarla

È il percorso consigliato sui PC compatibili, perché consente a Windows e WSL di raggiungersi tramite `127.0.0.1` senza esporre Ollama sulle altre interfacce.

La modalità mirrored richiede **Windows 11 22H2 o successivo** e una versione WSL aggiornata. Su Windows 10 usare il percorso NAT.

## 5. Creare `.wslconfig`

Da PowerShell:

```powershell
notepad $env:USERPROFILE\.wslconfig
```

Inserire:

```ini
[wsl2]
networkingMode=mirrored
```

Salvare, quindi arrestare completamente WSL:

```powershell
wsl --shutdown
```

Riaprire Ubuntu.

## 6. Test dal lato Linux

Da WSL:

```bash
curl http://127.0.0.1:11434/api/version
curl http://127.0.0.1:11434/api/tags
```

Impostare:

```bash
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
```

Verificare:

```bash
curl "$OLLAMA_BASE_URL/api/tags"
```

Se il test funziona, usare questo percorso nei laboratori.

---

# Fallback — rete NAT

## 7. Quando usarlo

Usare il fallback NAT quando:

- mirrored non è disponibile;
- una policy aziendale lo impedisce;
- mirrored non funziona correttamente sul PC;
- non si vuol creare/modificare il file `.wslconfig`.

In modalità NAT, `127.0.0.1` dentro WSL indica WSL, non il servizio Windows.

## 8. Rendere Ollama raggiungibile dalla rete virtuale

Per impostazione predefinita Ollama ascolta su `127.0.0.1:11434`. Il processo WSL, usando l'IP Windows, viene visto come connessione di rete.

In Windows impostare la variabile utente:

```powershell
[Environment]::SetEnvironmentVariable(
  "OLLAMA_HOST",
  "0.0.0.0:11434",
  "User"
)
```

Poi:

1. chiudere completamente Ollama dall'area di notifica;
2. riavviarlo dal menu Start;
3. verificare da PowerShell:

```powershell
curl.exe http://localhost:11434/api/tags
```

## 9. Ricavare l'IP Windows da WSL

```bash
WINDOWS_HOST=$(ip route show | awk '/default/ {print $3; exit}')
echo "$WINDOWS_HOST"
```

Impostare l'endpoint:

```bash
export OLLAMA_BASE_URL="http://$WINDOWS_HOST:11434"
```

Testare:

```bash
curl "$OLLAMA_BASE_URL/api/version"
curl "$OLLAMA_BASE_URL/api/tags"
```

## 10. Firewall

Se PowerShell raggiunge Ollama ma `curl` Linux verso l'IP Windows va in timeout, il firewall può bloccare la connessione.

Preferire queste opzioni, in ordine:

1. usare mirrored;
2. autorizzare la porta `11434` soltanto sul profilo **Privato**;
3. limitare la regola alla rete virtuale WSL quando l'ambiente lo consente;
4. non aprire la porta sulle reti pubbliche;
5. non configurare port forwarding Internet.

L'uso di `0.0.0.0:11434` amplia il binding. Va adottato soltanto per il fallback NAT.

## 11. Ripristinare il binding locale dopo il laboratorio

Da PowerShell:

```powershell
[Environment]::SetEnvironmentVariable(
  "OLLAMA_HOST",
  $null,
  "User"
)
```

Chiudere e riavviare Ollama.

---

## 12. Albero decisionale

```text
Ollama risponde in PowerShell?
│
├── NO → avviare/correggere Ollama Windows
│
└── SÌ
    │
    ├── curl Linux verso 127.0.0.1 funziona?
    │   └── SÌ → mirrored pronto
    │
    └── NO
        │
        ├── configurare/aggiornare mirrored
        │
        └── oppure usare NAT:
            OLLAMA_HOST=0.0.0.0:11434
            + IP host Windows
            + firewall limitato
```

## 13. Test finale obbligatorio

Da WSL:

```bash
curl "$OLLAMA_BASE_URL/api/tags"
python3 -c 'import os; print(os.environ.get("OLLAMA_BASE_URL"))'
```

Il setup è completo soltanto quando `curl` Linux riesce a leggere l'API Windows.

## Fonti ufficiali

- Microsoft — Accessing network applications with WSL: https://learn.microsoft.com/windows/wsl/networking
- Microsoft — Advanced settings configuration in WSL: https://learn.microsoft.com/windows/wsl/wsl-config
- Microsoft — Basic commands for WSL: https://learn.microsoft.com/windows/wsl/basic-commands
- Ollama — Windows: https://docs.ollama.com/windows
- Ollama — FAQ e `OLLAMA_HOST`: https://docs.ollama.com/faq
- Ollama — API introduction: https://docs.ollama.com/api/introduction

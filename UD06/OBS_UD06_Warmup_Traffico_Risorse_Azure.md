# OBS UD06 - Preparazione carico sulle risorse Azure

## Scopo

Questo file contiene una breve attività preliminare da eseguire prima del laboratorio autonomo UD06.

L'obiettivo è generare traffico controllato sulle risorse create in UD05, in modo da avere segnali osservabili durante l'analisi successiva.

I segnali attesi riguardano principalmente:

| Risorsa | Segnali attesi |
|---|---|
| Storage Account con static website | richieste HTTP, transazioni, eventuali richieste non riuscite |
| App Service | richieste HTTP, codici di stato, tempi di risposta |
| VM Linux | stato runtime e, solo se autorizzato, breve carico CPU |
| Azure Monitor | metriche aggiornate dopo alcuni minuti |

Questa attività non crea nuove risorse e non elimina risorse esistenti.

---

## Regole operative

Eseguire i comandi da **WSL o terminale locale**, dentro la cartella del repository della UD06.

Non eseguire questi comandi da Azure Cloud Shell se l'obiettivo è salvare file in `logs/` o `evidence/`, perché Cloud Shell è un ambiente remoto e non scrive automaticamente nel repository locale.

Prima di iniziare, posizionarsi nella cartella della UD06.

Esempio:

```bash
# Spostarsi nella cartella della UD06.
# Sostituire il percorso con quello reale del proprio repository.
cd ~/percorso/del/repository/UD06
```

Creare le cartelle locali, se non esistono:

```bash
# Crea le cartelle usate per evidenze, report e log locali.
mkdir -p docs evidence logs
```

---

## 1. Impostare le variabili

Sostituire `<codice>` con il proprio codice partecipante.

Se una risorsa non è stata creata durante UD05, lasciare vuota la relativa variabile.

```bash
# Resource Group creato in UD05.
export RG_NAME="rg-obs-ud05-<codice>"

# Storage Account usato per lo static website.
export STORAGE_NAME="stobsud05<codice>01"

# App Service creato in UD05.
export APP_NAME="app-obs-ud05-<codice>"

# VM Linux creata o analizzata in UD05.
# Lasciare vuoto se la VM non è presente.
export VM_NAME="vm-obs-ud05-<codice>"
```

Verificare i valori:

```bash
# Mostra le variabili impostate.
printf 'RG_NAME=%s\n' "$RG_NAME"
printf 'STORAGE_NAME=%s\n' "$STORAGE_NAME"
printf 'APP_NAME=%s\n' "$APP_NAME"
printf 'VM_NAME=%s\n' "$VM_NAME"
```

Verificare il contesto Azure:

```bash
# Mostra la subscription attualmente selezionata.
az account show --output table
```

---

## 2. Generare traffico sullo Storage static website

Questa sezione genera richieste HTTP verso l'endpoint static website dello Storage Account.

Le richieste dovrebbero contribuire alle metriche dello Storage Account, ad esempio transazioni e traffico.

Saltare questa sezione se lo Storage Account non è presente o se lo static website non è stato abilitato.

```bash
# Recupera l'endpoint Web primario dello Storage Account.
# L'endpoint viene salvato in una variabile locale.
export STORAGE_WEB_URL="$(az storage account show \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --query "primaryEndpoints.web" \
  --output tsv)"

# Salva l'endpoint in un file di log locale.
echo "STORAGE_WEB_URL=$STORAGE_WEB_URL" | tee logs/ud06_storage_endpoint.log
```

Verificare che la variabile non sia vuota:

```bash
# Visualizza l'endpoint dello static website.
printf 'STORAGE_WEB_URL=%s\n' "$STORAGE_WEB_URL"
```

Generare richieste verso `index.html`:

```bash
# Genera richieste HTTP verso il file index.html.
# Il parametro warmup rende le richieste distinguibili.
for i in $(seq 1 40); do
  curl -s -o /dev/null \
    -w "storage index request $i -> HTTP %{http_code}, time %{time_total}s\n" \
    "${STORAGE_WEB_URL}index.html?warmup=$i" \
    | tee -a logs/ud06_storage_traffic.log

  sleep 1
done
```

Generare alcune richieste verso file non esistenti:

```bash
# Genera richieste verso file non presenti.
# Queste richieste possono produrre codici HTTP diversi da 200.
for i in $(seq 1 10); do
  curl -s -o /dev/null \
    -w "storage missing request $i -> HTTP %{http_code}, time %{time_total}s\n" \
    "${STORAGE_WEB_URL}missing-ud06-$i.html" \
    | tee -a logs/ud06_storage_traffic.log

  sleep 1
done
```

---

## 3. Generare richieste sull'App Service

Questa sezione genera richieste HTTP verso l'App Service.

Le richieste dovrebbero contribuire alle metriche dell'App Service, ad esempio numero richieste, tempi di risposta e codici HTTP.

Saltare questa sezione se l'App Service non è presente.

```bash
# Recupera il default hostname dell'App Service.
export APP_HOST="$(az webapp show \
  --name "$APP_NAME" \
  --resource-group "$RG_NAME" \
  --query "defaultHostName" \
  --output tsv)"

# Costruisce l'URL HTTPS dell'App Service.
export APP_URL="https://${APP_HOST}"

# Salva l'URL in un file di log locale.
echo "APP_URL=$APP_URL" | tee logs/ud06_appservice_endpoint.log
```

Verificare l'URL:

```bash
# Visualizza l'URL dell'App Service.
printf 'APP_URL=%s\n' "$APP_URL"
```

Generare richieste verso la home page:

```bash
# Genera richieste verso la home page dell'App Service.
for i in $(seq 1 50); do
  curl -s -o /dev/null \
    -w "app home request $i -> HTTP %{http_code}, time %{time_total}s\n" \
    "${APP_URL}/?warmup=$i" \
    | tee -a logs/ud06_appservice_traffic.log

  sleep 1
done
```

Generare alcune richieste verso percorsi non esistenti:

```bash
# Genera richieste verso path non presenti.
# Queste richieste possono produrre 404 o altri codici HTTP.
for i in $(seq 1 10); do
  curl -s -o /dev/null \
    -w "app missing request $i -> HTTP %{http_code}, time %{time_total}s\n" \
    "${APP_URL}/missing-ud06-$i" \
    | tee -a logs/ud06_appservice_traffic.log

  sleep 1
done
```

---

## 4. Verificare lo stato della VM

Questa sezione controlla lo stato della VM senza avviarla.

Non avviare la VM se non è stato richiesto dal docente.

```bash
# Mostra lo stato runtime della VM.
# Il comando non avvia la VM e non modifica la risorsa.
az vm get-instance-view \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --query "instanceView.statuses[].{code:code,displayStatus:displayStatus}" \
  --output table \
  | tee logs/ud06_vm_state.log
```

---

## 5. Carico leggero sulla VM, solo se autorizzato

Eseguire questa sezione solo se il docente conferma che:

```text
[ ] la VM è presente
[ ] la VM è Running
[ ] è consentito generare un breve carico CPU
```

Il comando seguente usa Azure Run Command per eseguire un breve ciclo CPU sulla VM.

Non apre porte di rete e non richiede accesso SSH.

```bash
# Eseguire solo se autorizzato dal docente.
# Il comando genera carico CPU per circa 45 secondi.
az vm run-command invoke \
  --name "$VM_NAME" \
  --resource-group "$RG_NAME" \
  --command-id RunShellScript \
  --scripts "timeout 45 bash -c 'while true; do :; done'" \
  --output json > evidence/ud06_vm_cpu_warmup.json
```

---

## 6. Attendere l'aggiornamento delle metriche

Azure Monitor può richiedere alcuni minuti prima di mostrare i nuovi valori metrici.

Dopo aver eseguito il carico, attendere almeno 5 minuti prima di analizzare le metriche dal Portale o da CLI.

```bash
# Salva un timestamp locale di completamento dell'attività.
echo "Warm-up completato alle $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  | tee logs/ud06_warmup_completed.log

# Messaggio operativo.
echo "Attendere 5-10 minuti prima di leggere le metriche da Portale Azure o da CLI."
```

---

## 7. Controllare i file prodotti localmente

```bash
# Elenca i file prodotti in logs/ ed evidence/.
find logs evidence -maxdepth 2 -type f | sort
```

Output atteso, in base alle risorse presenti:

```text
logs/ud06_storage_endpoint.log
logs/ud06_storage_traffic.log
logs/ud06_appservice_endpoint.log
logs/ud06_appservice_traffic.log
logs/ud06_vm_state.log
logs/ud06_warmup_completed.log
```

---

## 8. Cosa osservare dopo il warm-up

Dopo alcuni minuti, nel laboratorio autonomo UD06 controllare:

| Risorsa | Dove osservare | Segnali attesi |
|---|---|---|
| Storage Account | Portale Azure -> Storage Account -> Metrics | transazioni, traffico, eventuali errori |
| App Service | Portale Azure -> App Service -> Metrics | richieste, tempi di risposta, codici HTTP |
| VM | Portale Azure -> VM -> Metrics | CPU, stato runtime, eventuale rete |
| Azure CLI | comandi `az monitor metrics list` | output JSON salvabile in `evidence/` |

---

## 9. Nota importante

Questa attività genera traffico e quindi metriche di piattaforma sulle risorse Azure.

Non genera automaticamente log in Log Analytics.

Per inviare log a Log Analytics servono configurazioni specifiche, ad esempio Diagnostic Settings, agenti o integrazioni applicative. Questi aspetti vengono trattati nelle UD successive.

# OBS UD05 - Appendice
# Installazione di Azure CLI in WSL

## Scopo della sezione

Questa appendice serve a preparare l'ambiente WSL per usare Azure CLI durante la UD05 e le UD successive.

Nel laboratorio produciamo file di evidenza dentro il repository locale, nelle cartelle:

```text
docs/
evidence/
logs/
```

Per questo motivo i comandi che salvano output con redirection, ad esempio:

```bash
az account show --output json > evidence/ud05_account_context.json
```

devono essere eseguiti preferibilmente da WSL o da un terminale locale posizionato nella cartella del repository.

Azure Cloud Shell è utile per verifiche rapide dal Portale Azure, ma i file creati lì restano nell'ambiente remoto di Cloud Shell. Non finiscono automaticamente nel repository locale del partecipante.

---

## 1. Che cos'è Azure CLI

Azure CLI è lo strumento da riga di comando che permette di lavorare con Azure usando il comando:

```bash
az
```

Nel nostro laboratorio la useremo soprattutto per:

- verificare il contesto Azure;
- leggere informazioni su subscription, Resource Group e risorse;
- salvare output JSON nelle evidenze;
- preparare materiale da usare nella UD06.

In UD05 la creazione delle risorse resta principalmente tramite Portale Azure. La CLI viene usata come supporto di verifica e documentazione.

---

## 2. Verificare di essere in WSL

Aprire il terminale WSL, ad esempio Ubuntu.

Eseguire:

```bash
# Mostra informazioni sul kernel Linux in uso.
# Se siamo in WSL, l'output contiene riferimenti a Linux e spesso anche a Microsoft/WSL.
uname -a
```

Verificare anche la distribuzione Linux:

```bash
# Mostra nome e versione della distribuzione Linux.
# È utile per capire se stiamo usando Ubuntu, Debian o un'altra distribuzione.
lsb_release -a
```

Esempio di output atteso:

```text
Distributor ID: Ubuntu
Description:    Ubuntu 22.04...
Codename:       jammy
```

---

## 3. Verificare se Azure CLI è già installata

Eseguire:

```bash
# Mostra la versione di Azure CLI, se il comando az è disponibile.
az version
```

Se Azure CLI è già installata, verrà mostrato un output JSON simile a questo:

```json
{
  "azure-cli": "2.xx.x",
  "azure-cli-core": "2.xx.x",
  "azure-cli-telemetry": "1.x.x",
  "extensions": {}
}
```

Se invece compare un errore simile a:

```text
az: command not found
```

Azure CLI non è installata e bisogna procedere con la sezione successiva.

---

## 4. Installare Azure CLI in WSL Ubuntu/Debian

Eseguire i comandi seguenti dentro WSL.

### 4.1 Aggiornare l'indice dei pacchetti e installare prerequisiti

```bash
# Aggiorna l'elenco dei pacchetti disponibili.
sudo apt-get update

# Installa pacchetti necessari per usare repository HTTPS,
# scaricare file, gestire chiavi e riconoscere la versione della distribuzione.
sudo apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release
```

### 4.2 Aggiungere la chiave Microsoft

```bash
# Crea la directory in cui vengono conservate le chiavi dei repository.
sudo mkdir -p /etc/apt/keyrings

# Scarica la chiave Microsoft e la converte nel formato usato da apt.
curl -sLS https://packages.microsoft.com/keys/microsoft.asc \
  | gpg --dearmor \
  | sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null

# Imposta permessi di lettura adeguati sulla chiave.
sudo chmod go+r /etc/apt/keyrings/microsoft.gpg
```

### 4.3 Aggiungere il repository Azure CLI

```bash
# Ricava il nome in codice della distribuzione, ad esempio jammy o noble.
AZ_DIST=$(lsb_release -cs)

# Crea il file di configurazione del repository Azure CLI.
echo "Types: deb
URIs: https://packages.microsoft.com/repos/azure-cli/
Suites: ${AZ_DIST}
Components: main
Architectures: $(dpkg --print-architecture)
Signed-by: /etc/apt/keyrings/microsoft.gpg" \
| sudo tee /etc/apt/sources.list.d/azure-cli.sources
```

### 4.4 Installare Azure CLI

```bash
# Aggiorna nuovamente l'elenco dei pacchetti includendo il repository Microsoft.
sudo apt-get update

# Installa Azure CLI.
sudo apt-get install -y azure-cli
```

---

## 5. Verificare l'installazione

Eseguire:

```bash
# Controlla che Azure CLI sia installata e mostra la versione.
az version
```

Oppure:

```bash
# Variante sintetica del controllo versione.
az --version
```

Se viene mostrata la versione di Azure CLI, l'installazione è completata.

---

## 6. Accedere ad Azure da WSL

Eseguire:

```bash
# Avvia l'accesso interattivo ad Azure.
# Normalmente apre una procedura tramite browser.
az login
```

Dopo l'accesso, verificare il contesto Azure:

```bash
# Mostra la subscription attualmente selezionata in forma tabellare.
az account show --output table
```

Se sono presenti più subscription, visualizzarle con:

```bash
# Elenca le subscription disponibili per l'account autenticato.
az account list --output table
```

Per selezionare la subscription corretta:

```bash
# Imposta la subscription da usare nei comandi successivi.
# Sostituire il valore tra virgolette con nome o ID della subscription.
az account set --subscription "<nome-o-id-subscription>"
```

Verificare di nuovo:

```bash
# Conferma che la subscription attiva sia quella corretta.
az account show --output table
```

---

## 7. Posizionarsi nel repository locale della UD05

Prima di salvare file in `evidence/`, dobbiamo essere nella cartella del repository locale.

Esempio:

```bash
# Spostarsi nella cartella del repository del corso.
# Il percorso è solo un esempio e va adattato al proprio ambiente.
cd ~/academy-observability/<nome-repository>
```

Verificare il percorso corrente:

```bash
# Mostra la directory in cui ci troviamo.
pwd
```

Creare le cartelle di lavoro, se non esistono:

```bash
# Crea le cartelle usate per report, evidenze e log.
mkdir -p docs evidence logs
```

---

## 8. Salvare il contesto Azure nel repository locale

Eseguire da WSL, dentro la cartella del repository:

```bash
# Salva il contesto Azure completo in formato JSON dentro la cartella evidence.
az account show --output json > evidence/ud05_account_context.json
```

Verificare che il file sia stato creato:

```bash
# Controlla che il file JSON sia presente nella cartella evidence.
ls -l evidence/ud05_account_context.json
```

Visualizzare una versione sintetica del contesto:

```bash
# Mostra solo i campi principali: nome subscription, ID, tenant e utente.
az account show \
  --query "{name:name,id:id,tenantId:tenantId,user:user.name}" \
  --output table
```

Nel report compilare:

```text
Subscription:
Tenant:
Utente:
Data/ora:
Modalità usata: Azure CLI locale in WSL
```

---

## 9. Differenza tra WSL e Azure Cloud Shell

| Ambiente | Dove vengono creati i file | Uso consigliato nel laboratorio |
|---|---|---|
| WSL | Nel repository locale del partecipante | Comandi che salvano file in `docs/`, `evidence/`, `logs/` |
| Azure Cloud Shell | Nell'ambiente remoto Cloud Shell | Verifiche rapide, comandi esplorativi, output da copiare |
| Portale Azure | Nel browser | Creazione e verifica visuale delle risorse |

Regola pratica:

```text
Se il comando contiene > evidence/nome_file.json,
deve essere eseguito da WSL o da un terminale locale nella cartella del repository.
```

Esempio corretto da WSL:

```bash
# Eseguito da WSL nella cartella del repository locale.
az account show --output json > evidence/ud05_account_context.json
```

Esempio da evitare in Cloud Shell, se ci aspettiamo che il file finisca nel repository locale:

```bash
# In Cloud Shell il comando crea il file nell'ambiente remoto di Cloud Shell,
# non nel repository locale del partecipante.
az account show --output json > evidence/ud05_account_context.json
```

---

## 10. Uso accettabile di Cloud Shell nella UD05

Cloud Shell può essere usata per controlli rapidi, ad esempio:

```bash
# Mostra una vista sintetica del contesto Azure direttamente in Cloud Shell.
az account show \
  --query "{name:name,id:id,tenantId:tenantId,user:user.name}" \
  --output table
```

In questo caso il partecipante deve:

1. copiare i valori principali nel report locale;
2. salvare uno screenshot del Portale o di Cloud Shell, se richiesto;
3. non dare per scontato che eventuali file creati in Cloud Shell siano presenti nel repository locale.

Evidenza consigliata:

```text
evidence/01_subscription_context.png
```

---

## 11. Controllo finale prima di proseguire

Eseguire da WSL nella cartella del repository:

```bash
# Mostra la directory corrente.
pwd
```

Verificare che siano presenti i file prodotti:

```bash
# Elenca i file presenti nelle cartelle di lavoro del laboratorio.
find docs evidence logs -maxdepth 2 -type f | sort
```

Verificare che compaia almeno:

```text
evidence/ud05_account_context.json
```

Controllare lo stato Git:

```bash
# Mostra file nuovi, modificati o non tracciati.
git status
```

Il file `evidence/ud05_account_context.json` dovrebbe comparire tra i file nuovi o modificati.

---

## 12. Problemi comuni

| Problema | Possibile causa | Azione |
|---|---|---|
| `az: command not found` | Azure CLI non installata o shell non aggiornata | Installare Azure CLI, poi chiudere e riaprire WSL |
| `az login` non completa l'accesso | Problema browser, MFA o sessione | Riprovare e verificare account usato |
| `az account show` non mostra subscription | Account errato o subscription non selezionata | Usare `az account list --output table` e poi `az account set` |
| File non trovato in `evidence/` | Comando eseguito in Cloud Shell invece che in WSL | Rieseguire il comando da WSL nella cartella del repository |
| Accesso negato con `sudo apt-get` | Password WSL errata o utente senza privilegi | Verificare utente WSL e privilegi `sudo` |
| Repository non trovato | Percorso locale errato | Usare `pwd`, `ls` e spostarsi nella cartella corretta |

---

## 13. Aggiornare Azure CLI

Durante il laboratorio non aggiornare strumenti se non necessario. Gli aggiornamenti vanno fatti con criterio, non nel mezzo di una procedura che deve produrre evidenze.

Per aggiornare Azure CLI con `apt`:

```bash
# Aggiorna l'elenco dei pacchetti disponibili.
sudo apt-get update

# Aggiorna solo il pacchetto azure-cli.
sudo apt-get install --only-upgrade -y azure-cli
```

In alternativa:

```bash
# Avvia la procedura di aggiornamento gestita da Azure CLI.
az upgrade
```

Dopo l'aggiornamento:

```bash
# Verifica la versione installata dopo l'aggiornamento.
az version
```

---

## 14. Fonti ufficiali utili

Documentazione Microsoft Learn per installazione Azure CLI su Linux:

```text
https://learn.microsoft.com/cli/azure/install-azure-cli-linux
```

Documentazione Microsoft Learn per autenticazione Azure CLI:

```text
https://learn.microsoft.com/cli/azure/authenticate-azure-cli
```

Documentazione Microsoft Learn per gestione subscription con Azure CLI:

```text
https://learn.microsoft.com/cli/azure/manage-azure-subscriptions-azure-cli
```

---

## 15. Risultato atteso

Al termine di questa appendice il partecipante dovrebbe avere:

```text
[ ] Azure CLI installata in WSL
[ ] accesso Azure eseguito con az login
[ ] subscription corretta selezionata
[ ] cartelle docs, evidence e logs presenti nel repository locale
[ ] file evidence/ud05_account_context.json creato da WSL
[ ] differenza tra WSL e Cloud Shell compresa
[ ] git status verificato prima di proseguire
```

# UD14 - Guida operativa
## Debug pipeline multistage, ACR, ACI e smoke test

---

# 1. Scopo della guida

Questa guida serve come supporto rapido durante il laboratorio UD14.

La pipeline è divisa in stage. Per risolvere un problema dobbiamo prima capire **in quale stage** avviene l'errore.

---

# 2. La pipeline non parte

Possibili cause:

- file YAML non presente su GitHub;
- path YAML sbagliato;
- pipeline collegata al repository errato;
- trigger non attivo;
- GitHub non autorizzato.

Verifiche:

```bash
git status
git log --oneline -5
```

Controllare su GitHub che esista:

```text
work/UD14/azure-pipelines.yml
```

Nel portale Azure DevOps verificare che la pipeline punti a quel path.

---

# 3. Lo stage ValidateRepository fallisce

Possibili cause:

- cartella `work/UD14` non presente;
- file mancanti;
- valore `workDir` errato;
- errore sintattico in `src/app.py`.

Verifica locale:

```bash
cd work/UD14
find . -maxdepth 2 -type f | sort
python3 -m py_compile src/app.py
```

File minimi attesi:

```text
src/app.py
requirements.txt
Dockerfile
.dockerignore
azure-pipelines.yml
```

---

# 4. Lo stage BuildAndPush fallisce

Possibili cause:

- Dockerfile errato;
- `requirements.txt` errato;
- contesto di build sbagliato;
- nome ACR errato;
- service connection senza permessi;
- login ACR fallito.

Verifica locale:

```bash
cd work/UD14
docker build -t obsapp-ud14:test .
```

Verifica Azure:

```bash
az acr show \
  --name NOME_ACR \
  --resource-group NOME_RESOURCE_GROUP
```

---

# 5. Il push su ACR fallisce

Possibili cause:

- ACR inesistente;
- nome ACR scritto male;
- service connection Azure non corretta;
- permessi insufficienti;
- `az acr login` non riuscito.

Verifica:

```bash
az acr login --name NOME_ACR
```

Controllo tag:

```bash
az acr repository show-tags \
  --name NOME_ACR \
  --repository obsapp-ud14 \
  -o table
```

---

# 6. Lo stage DeployToACI fallisce

Possibili cause:

- Resource Group errato;
- DNS label già usata;
- credenziali ACR non disponibili;
- admin account ACR non abilitato;
- immagine non trovata;
- porta errata.

Verifiche:

```bash
az group show --name NOME_RESOURCE_GROUP
az acr credential show --name NOME_ACR
```

Se le credenziali ACR non sono disponibili:

```bash
az acr update \
  --name NOME_ACR \
  --admin-enabled true
```

Se il DNS label è già usato, cambiare:

```yaml
aciDnsName: 'obsapp-ud14-NOMEUNIVOCO'
```

---

# 7. Lo stage SmokeTest fallisce

Possibili cause:

- container ancora in avvio;
- FQDN non disponibile;
- porta errata;
- app non avviata correttamente;
- endpoint sbagliato;
- warm-up insufficiente.

Verifica stato container:

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --query "{state:instanceView.state,fqdn:ipAddress.fqdn,ports:ipAddress.ports}" \
  -o json
```

Verifica log:

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI
```

Se il container impiega più tempo ad avviarsi, aumentare temporaneamente:

```bash
sleep 20
```

a:

```bash
sleep 30
```

---

# 8. Attenzione a `/error`

L'endpoint `/error` restituisce volutamente `500`.

Quindi questo comando fallisce per definizione:

```bash
curl --fail http://FQDN:8000/error
```

Questo è normale.

`/error` serve per generare un errore controllato e leggere i log. Non deve essere usato come smoke test bloccante.

---

# 9. L'app risponde manualmente ma lo smoke test fallisce

Possibili cause:

- la pipeline testa troppo presto;
- nella pipeline viene costruito un URL sbagliato;
- `containerPort` non coincide con la porta dell'app;
- il FQDN recuperato è vuoto.

Verificare nei log dello stage `SmokeTest`:

```text
APP_URL=http://...
```

E confrontare con il comando manuale:

```bash
curl http://$FQDN:8000/health
```

---

# 10. I log sono vuoti

Possibili cause:

- non è stato generato traffico;
- stai guardando il container sbagliato;
- il container è stato appena creato;
- l'app non scrive su stdout.

Generare traffico:

```bash
curl http://$FQDN:8000/health
curl http://$FQDN:8000/error
```

Poi leggere:

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI
```

---

# 11. Comandi rapidi utili

## Stato ACI

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --query "{state:instanceView.state,fqdn:ipAddress.fqdn}" \
  -o table
```

## FQDN

```bash
az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --query ipAddress.fqdn \
  -o tsv
```

## Log ACI

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI
```

## Tag ACR

```bash
az acr repository show-tags \
  --name NOME_ACR \
  --repository obsapp-ud14 \
  -o table
```

## Eliminazione ACI

```bash
az container delete \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --yes
```

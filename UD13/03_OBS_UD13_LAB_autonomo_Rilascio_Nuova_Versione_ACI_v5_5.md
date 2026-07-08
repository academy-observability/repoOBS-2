# UD13 - Laboratorio autonomo
## Rilascio di una nuova versione su ACI tramite pipeline

---

# Scenario

L'applicazione è stata deployata su ACI tramite pipeline. Ora devi simulare una nuova release applicativa.

Non devi creare una nuova pipeline. Devi modificare la versione dell'applicazione, fare commit/push e dimostrare che il ciclo automatico produce una nuova immagine e un nuovo deploy.

---

# Obiettivo

Dimostrare il flusso:

```text
modifica codice
  -> commit
  -> push
  -> pipeline
  -> nuova immagine in ACR
  -> nuovo container ACI
  -> test HTTP
  -> log cloud
```

---

# Task 1 - Modifica versione applicativa

Apri il file:

```bash
code work/UD13/src/app.py
```

Modifica il valore di default della versione:

```python
APP_VERSION = os.getenv("APP_VERSION", "1.0")
```

in:

```python
APP_VERSION = os.getenv("APP_VERSION", "1.1")
```

Nota: se la pipeline passa `APP_VERSION` come variabile d'ambiente, quella variabile può sovrascrivere il valore di default. In questo caso modifica anche nel file `azure-pipelines.yml`:

```yaml
appVersion: '1.1'
```

---

# Task 2 - Commit e push

```bash
git status
git add work/UD13
git commit -m "UD13 - rilascio versione 1.1"
git push
```

---

# Task 3 - Verifica nuovo run pipeline

Nel portale Azure DevOps verifica:

- nuovo run avviato;
- stato finale `Succeeded`;
- nuovo `Build.BuildId`;
- nuovo push immagine;
- nuovo deploy ACI.

---

# Task 4 - Verifica nuovo tag in ACR

```bash
az acr repository show-tags \
  --name NOME_ACR_UNIVOCO \
  --repository obsapp-ud13 \
  -o table
```

Individua il tag più recente.

---

# Task 5 - Test applicativo

Recupera il FQDN:

```bash
FQDN=$(az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --query ipAddress.fqdn \
  -o tsv)
```

Esegui:

```bash
curl http://$FQDN:8000/
curl http://$FQDN:8000/health
curl http://$FQDN:8000/error
```

Nella risposta deve essere visibile la versione aggiornata o comunque deve essere dimostrabile il nuovo deployment tramite tag immagine e log pipeline.

---

# Task 6 - Log cloud

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13
```

Individua almeno una riga di log relativa ai test appena eseguiti.

---

# Evidenze richieste

Nel file `docs/evidence_ud13.md` aggiungi:

1. commit della modifica;
2. numero del nuovo run pipeline;
3. tag immagine generato;
4. output del test `/` o `/health`;
5. alcune righe di log cloud;
6. breve spiegazione del ciclo modifica -> pipeline -> deploy.

---

# Cleanup

Se indicato dal docente, elimina il container ACI:

```bash
az container delete \
  --resource-group NOME_RESOURCE_GROUP \
  --name aci-obsapp-ud13 \
  --yes
```

Non eliminare ACR salvo indicazione esplicita.

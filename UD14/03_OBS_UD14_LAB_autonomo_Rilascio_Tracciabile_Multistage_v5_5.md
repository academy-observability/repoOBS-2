# UD14 - Laboratorio autonomo
## Rilascio tracciabile con pipeline multistage

---

# 1. Scenario

Hai una pipeline multistage funzionante che valida il repository, costruisce l'immagine, la pubblica in ACR, la distribuisce su ACI e verifica gli endpoint principali.

Ora devi dimostrare che il rilascio è tracciabile.

Devi produrre una nuova versione dell'applicazione e verificare la coerenza tra:

```text
run pipeline -> Build ID -> tag ACR -> risposta HTTP -> log cloud
```

---

# 2. Attività richieste

## 2.1 Modifica applicativa

Modifica un valore visibile nella risposta dell'applicazione.

Esempio: modifica il default di `APP_VERSION` nel file `src/app.py`, oppure aggiungi una piccola informazione testuale nella risposta di `/`.

La modifica deve essere riconoscibile con:

```bash
curl http://FQDN:8000/
```

---

## 2.2 Commit e push

Esegui:

```bash
git status
git add work/UD14
git commit -m "UD14 - nuova versione tracciabile"
git push
```

---

## 2.3 Esecuzione pipeline

Avvia o attendi l'esecuzione della pipeline UD14.

Annota:

```text
Nome pipeline:
Run number:
Build ID:
Esito finale:
```

---

## 2.4 Verifica tag in ACR

Esegui:

```bash
az acr repository show-tags \
  --name NOME_ACR \
  --repository obsapp-ud14 \
  -o table
```

Individua il tag corrispondente al nuovo Build ID.

---

## 2.5 Verifica ACI

Recupera il FQDN:

```bash
FQDN=$(az container show \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI \
  --query ipAddress.fqdn \
  -o tsv)

echo $FQDN
```

Verifica:

```bash
curl http://$FQDN:8000/
curl http://$FQDN:8000/health
```

---

## 2.6 Verifica smoke test

Nel portale Azure DevOps apri lo stage `SmokeTest` e verifica che abbia controllato correttamente gli endpoint.

Annota gli endpoint testati.

---

## 2.7 Lettura log cloud

Genera traffico:

```bash
curl http://$FQDN:8000/health
curl http://$FQDN:8000/error
```

Leggi i log:

```bash
az container logs \
  --resource-group NOME_RESOURCE_GROUP \
  --name NOME_ACI
```

Cerca nei log almeno:

```text
path
status
latency_ms
request_id
build_id
```

---

# 3. Evidenze da consegnare

Crea o aggiorna:

```text
docs/evidence_ud14.md
```

Aggiungi una sezione autonoma:

```md
## Laboratorio autonomo UD14

### 1. Modifica effettuata
Descrivo la modifica applicativa.

### 2. Pipeline run
Indico run, Build ID ed esito finale.

### 3. Tag ACR
Incollo output con il tag corrispondente.

### 4. Output applicativo
Incollo risposta di GET /.

### 5. Smoke test
Descrivo gli endpoint verificati dalla pipeline.

### 6. Log cloud
Incollo righe significative di az container logs.

### 7. Conclusione
Spiego perché il rilascio è tracciabile.
```

---

# 4. Criteri di riuscita

Il laboratorio autonomo è riuscito se puoi dimostrare che:

- esiste un nuovo commit;
- la pipeline è stata eseguita;
- esiste un nuovo Build ID;
- ACR contiene il tag corrispondente;
- ACI usa la nuova immagine;
- l'app risponde correttamente;
- lo smoke test è passato;
- i log cloud sono leggibili.

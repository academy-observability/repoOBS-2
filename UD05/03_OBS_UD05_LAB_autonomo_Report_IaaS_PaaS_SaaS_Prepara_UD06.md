# OBS_UD05 - Laboratorio autonomo

# Report IaaS/PaaS/SaaS e preparazione UD06

## 1. Obiettivo

Nel laboratorio autonomo completiamo la documentazione tecnica della UD05.

Non dobbiamo creare nuove risorse non previste.

Non dobbiamo eliminare le risorse create.

Obiettivi:

```text
classificare le risorse create o analizzate
documentare IaaS/PaaS/SaaS
completare l'analisi Marketplace SaaS
verificare Cost Management
salvare inventario per UD06
produrre il report finale
```

---

## 2. Regola no-cleanup

Prima di procedere, scrivere nel report:

```text
Confermo che non elimino le risorse UD05 prima della UD06.
```

Alla fine del laboratorio autonomo, ripetere la verifica.

Non eliminare:

```text
Resource Group
Storage Account
App Service
App Service Plan
Virtual Machine
Disk
Network Interface
Network Security Group
Virtual Network
Public IP, se presente
```

È consentito fermare/deallocare la VM solo se il docente lo richiede.

---

## 3. Nota su WSL, terminale locale e Cloud Shell

I comandi che salvano file nella cartella `evidence/` devono essere eseguiti nel repository locale, normalmente da WSL o da un terminale locale con Azure CLI installata e autenticata.

Azure Cloud Shell può essere usata per verifiche rapide, ma non scrive automaticamente nel repository locale.

Regola pratica:

```text
WSL/terminale locale: usare comandi con > evidence/...
Cloud Shell: usare viste tabellari, copiare output nel report o salvare screenshot.
```

Prima del commit finale verificare sempre da WSL:

```bash
# Elenca i file prodotti localmente.
find docs evidence -maxdepth 2 -type f | sort

# Mostra lo stato Git del repository.
git status
```

---

## 4. Preparazione

Verificare le cartelle locali:

```bash
# Crea le cartelle locali usate per report ed evidenze.
mkdir -p docs evidence
```

Impostare il Resource Group:

```bash
# Sostituire <codice> con il proprio codice partecipante.
export RG_NAME="rg-obs-ud05-<codice>"
```

Verificare l'esistenza del Resource Group:

```bash
# Verifica che il Resource Group sia visibile nella subscription attiva.
az group show \
  --name "$RG_NAME" \
  --output table
```

Se il comando fallisce, fermarsi e avvisare il docente.

---

## 5. Inventario risorse

### 5.1 Inventario da WSL o terminale locale

Eseguire dal repository locale:

```bash
# Salva l'elenco completo delle risorse del Resource Group in formato JSON.
az resource list \
  --resource-group "$RG_NAME" \
  --output json > evidence/08_rg_inventory_for_ud06.json
```

Vista sintetica:

```bash
# Mostra una tabella sintetica utile per il controllo in aula.
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{name:name,type:type,location:location}" \
  --output table
```

Salvare anche il controllo finale del Resource Group:

```bash
# Salva nome, regione e tag del Resource Group per dimostrare che è ancora presente.
az group show \
  --name "$RG_NAME" \
  --query "{name:name,location:location,tags:tags}" \
  --output json > evidence/ud05_rg_final_check.json
```

### 5.2 Variante Cloud Shell

In Cloud Shell eseguire solo viste sintetiche:

```bash
# In Cloud Shell non usare redirection verso evidence/ se il file deve finire nel repository locale.
RG_NAME="rg-obs-ud05-<codice>"

az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{name:name,type:type,location:location}" \
  --output table
```

Copiare i risultati principali nel report oppure salvare uno screenshot.

---

## 6. Report: risorse presenti

Nel report indicare:

```text
quante risorse sono presenti
quali tipi di risorse sono presenti
quali risorse sono principali
quali risorse sono collegate alla VM
quali risorse saranno utili in UD06
```

Tabella consigliata:

| Risorsa | Nome | Modello | Stato finale | Note costo |
|---|---|---|---|---|
| Storage Account |  | PaaS |  |  |
| App Service |  | PaaS |  |  |
| App Service Plan |  | PaaS |  |  |
| Virtual Machine |  | IaaS |  |  |
| Disk |  | IaaS collegata |  |  |
| Network Interface |  | IaaS collegata |  |  |
| Network Security Group |  | IaaS collegata |  |  |
| Virtual Network |  | IaaS collegata |  |  |
| Public IP |  | IaaS collegata |  |  |

---

## 7. Tabella IaaS/PaaS/SaaS

Compilare:

| Aspetto | VM IaaS | Storage static website PaaS | App Service PaaS | SaaS Marketplace |
|---|---|---|---|---|
| Cosa usa l'utente |  |  |  |  |
| Cosa configuriamo noi |  |  |  |  |
| Gestiamo OS |  |  |  |  |
| Gestiamo runtime |  |  |  |  |
| Gestiamo rete |  |  |  |  |
| Dove può nascere costo |  |  |  |  |
| Chi fa patching |  |  |  |  |
| Segnali utili per UD06 |  |  |  |  |

---

## 8. Analisi SaaS Marketplace

Scegliere un'offerta SaaS.

Non sottoscrivere.

Fermarsi prima di:

```text
Subscribe
Buy
Get it now
Create
Start trial
```

Compilare:

| Campo | Risposta |
|---|---|
| Nome offerta |  |
| Publisher |  |
| Categoria |  |
| Pricing visibile |  |
| Trial disponibile |  |
| Richiede account esterno |  |
| Dati trattati |  |
| Chi gestisce infrastruttura |  |
| Chi gestisce aggiornamenti |  |
| Rischio lock-in |  |
| Perché è SaaS |  |

Salvare evidenza:

```text
evidence/07_marketplace_saas_analysis.png
```

---

## 9. Cost Management finale

Aprire:

```text
Cost Management + Billing
```

Controllare:

```text
costi correnti
forecast
budget, se presente
risorse potenzialmente a costo
```

Annotare nel report:

```text
VM running o deallocated:
App Service Plan:
Storage Account:
Public IP:
Dischi:
```

Se il docente autorizza la deallocazione VM:

```text
VM -> Stop -> Stopped (deallocated)
```

Non eliminare la VM.

---

## 10. Verifica finale per UD06

Controllare che il Resource Group esista ancora:

```bash
# Salva il controllo finale nel repository locale.
az group show \
  --name "$RG_NAME" \
  --query "{name:name,location:location,tags:tags}" \
  --output json > evidence/ud05_rg_final_check.json
```

Controllare le risorse:

```bash
# Mostra una tabella sintetica delle risorse rimaste.
az resource list \
  --resource-group "$RG_NAME" \
  --query "[].{name:name,type:type}" \
  --output table
```

Salvare screenshot finale:

```text
evidence/09_no_cleanup_final_check.png
```

Nel report scrivere:

```text
Le risorse sono ancora presenti per UD06: Sì/No
```

---

## 11. Report da consegnare

Compilare:

```text
docs/report_ud05_azure_portal_iaas_paas_saas.md
```

Struttura:

```markdown
# Report UD05 - Azure Portal, IaaS, PaaS, SaaS

## 1. Contesto

Partecipante:
Codice:
Subscription:
Resource Group:
Regione:
Modalità CLI usata:
[ ] Azure CLI locale / WSL
[ ] Azure Cloud Shell

## 2. Vincolo UD06

Confermo che non elimino le risorse prima della UD06:
[ ] Sì
[ ] No

## 3. Risorse create o analizzate

| Risorsa | Nome | Modello | Stato finale |
|---|---|---|---|

## 4. Tabella IaaS/PaaS/SaaS

| Aspetto | VM IaaS | Storage PaaS | App Service PaaS | SaaS |
|---|---|---|---|---|

## 5. Analisi SaaS

Nome offerta:
Publisher:
Categoria:
Perché è SaaS:
Rischi:

## 6. Cost Management

Budget/overview:
Risorse con costo potenziale:
Azioni conservative eseguite:

## 7. Risorse lasciate per UD06

| Risorsa | Nome | Perché serve in UD06 |
|---|---|---|

## 8. Evidenze

- evidence/08_rg_inventory_for_ud06.json
- evidence/ud05_rg_final_check.json
- evidence/09_no_cleanup_final_check.png
- altre evidenze

## 9. Conclusioni

Differenza più chiara tra IaaS, PaaS e SaaS:
Cosa dovremo osservare in UD06:
```

---

## 12. Commit

Eseguire da WSL o terminale locale, nella cartella del repository:

```bash
# Controlla i file prodotti prima del commit.
git status

# Aggiunge report ed evidenze.
git add docs evidence

# Registra il lavoro nel repository.
git commit -m "Add UD05 autonomous IaaS PaaS SaaS report"

# Pubblica il lavoro sul repository remoto.
git push
```

---

## 13. Checklist finale

```text
[ ] report completato
[ ] tabella IaaS/PaaS/SaaS compilata
[ ] analisi SaaS completata senza sottoscrizione
[ ] Cost Management controllato
[ ] inventario UD06 salvato
[ ] screenshot no-cleanup salvato
[ ] risorse NON eliminate
[ ] commit/push eseguito, se richiesto
```

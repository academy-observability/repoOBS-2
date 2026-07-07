# OBS UD11 - Guida operativa
## Azure DevOps passo-passo per la UD11

Versione: v5.5  
Destinatari: partecipanti  
Tipo documento: guida operativa di supporto

---

# 1. Scopo della guida

Questa guida raccoglie i passaggi pratici minimi per completare UD11.

Non contiene comandi Docker, non contiene pipeline YAML e non contiene deploy su Azure.

Serve solo per preparare correttamente:

```text
Organizzazione Azure DevOps
Progetto Azure DevOps
Accesso a Pipelines
Accesso a Project settings
Individuazione Service connections
```

---

# 2. Accesso ad Azure DevOps

1. Apri il browser.
2. Accedi ad Azure DevOps.
3. Usa l'account indicato per il corso.
4. Verifica l'organizzazione attiva.

Annota:

```text
Account:
Organizzazione:
URL organizzazione:
```

---

# 3. Creazione organizzazione

Se non hai ancora una organizzazione:

1. scegli di creare una nuova organizzazione;
2. assegna un nome leggibile;
3. completa la procedura guidata;
4. verifica la URL finale.

Formato atteso:

```text
https://dev.azure.com/NOME_ORGANIZZAZIONE
```

Suggerimento:

```text
academy-observability-nomecognome
```

---

# 4. Creazione progetto

Dalla home dell'organizzazione crea il progetto.

Valori consigliati:

| Campo | Valore |
|---|---|
| Project name | `Observability-DevOps` |
| Visibility | `Private` |
| Version control | `Git` |
| Work item process | `Basic` |

Dopo la creazione, apri il progetto e verifica che il nome sia corretto.

---

# 5. Verifica Pipelines

Nel menu laterale del progetto cerca:

```text
Pipelines
```

Apri la sezione.

Risultato atteso:

- la sezione si apre;
- non è necessario creare una pipeline;
- puoi vedere il pulsante o l'opzione per crearne una.

Annota l'esito nel file di evidenza.

---

# 6. Verifica Project settings

Nel progetto cerca:

```text
Project settings
```

Apri la sezione.

Risultato atteso:

- la sezione si apre;
- puoi vedere impostazioni del progetto;
- puoi cercare la voce Service connections.

---

# 7. Verifica Service connections

Dentro Project settings cerca:

```text
Service connections
```

Non creare connessioni se il docente non lo richiede.

Devi solo sapere che qui, nelle prossime UD, verranno configurate connessioni verso:

- GitHub;
- Azure Resource Manager.

---

# 8. Controllo account GitHub

Apri GitHub e verifica l'account che userai per il corso.

Annota:

```text
Account GitHub:
Organizzazione/repository di riferimento:
```

Non creare repository nuovi se il docente non lo richiede.

---

# 9. Controllo riferimento Azure

Se conosci già la subscription o il Resource Group usati nel corso, annotali.

```text
Subscription:
Resource Group:
Regione:
Log Analytics Workspace:
```

Se non li conosci, scrivi:

```text
Da confermare nelle prossime UD
```

---

# 10. Checklist finale

Prima di concludere UD11 verifica:

| Controllo | OK |
|---|---|
| So accedere ad Azure DevOps |  |
| Ho una organizzazione Azure DevOps |  |
| Ho un progetto `Observability-DevOps` |  |
| Posso aprire Pipelines |  |
| Posso aprire Project settings |  |
| So dove sono le Service connections |  |
| So quale account GitHub userò |  |
| So distinguere GitHub, Azure DevOps, ACR e Azure |  |
| So che Docker operativo non fa parte della UD11 |  |

---

# 11. Errori frequenti

## 11.1 Creo più organizzazioni senza motivo

Evita di creare organizzazioni multiple se ne hai già una corretta.

## 11.2 Uso l'account sbagliato

Verifica sempre l'utente in alto a destra nel portale.

## 11.3 Confondo progetto e organizzazione

Ricorda:

```text
Organizzazione = contenitore generale
Progetto = area operativa specifica in cui creeremo pipeline e impostazioni
```

## 11.4 Cerco Docker in UD11

Docker operativo non è oggetto di UD11.

Arriverà in una attività successiva dedicata a Docker.

## 11.5 Cerco ACR o ACI in UD11

ACR e ACI saranno usati nelle UD successive.

In UD11 vanno capiti come concetti, non usati operativamente.

---

# 12. Output atteso

Alla fine devi avere:

```text
Organizzazione Azure DevOps verificata
Progetto Azure DevOps verificato
Accesso a Pipelines verificato
Accesso a Project settings verificato
File di evidenza compilato
```

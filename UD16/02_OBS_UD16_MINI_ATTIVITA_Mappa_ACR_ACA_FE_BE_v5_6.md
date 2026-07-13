# UD16 - Mini-attività
## Mappa ACR, ACA, frontend, backend

## 1. Completa la mappa

```text
GitHub repository
    |
    v
Azure DevOps pipeline UD15
    |
    v
Azure Container Registry
    |                         |
    v                         v
backend:<tag>              frontend:<tag>
    |                         |
    v                         v
Backend Container App      Frontend Container App
                              |
                              v
                        Utente / Browser / curl
```

Aggiungi nella mappa:

- ACA Environment;
- `BACKEND_URL`;
- FQDN backend;
- FQDN frontend;
- stage pipeline UD16.

## 2. Tabella da completare

| Elemento | Dove si trova | A cosa serve | Come lo verifico |
|---|---|---|---|
| ACR | | | |
| Immagine backend | | | |
| Immagine frontend | | | |
| ACA Environment | | | |
| Backend Container App | | | |
| Frontend Container App | | | |
| BACKEND_URL | | | |
| Revisione | | | |
| Log | | | |

## 3. Domande

1. Quale UD ha prodotto le immagini usate in UD16?
2. Perché UD16 non deve rifare la build delle immagini?
3. Dove si vede il FQDN del backend?
4. Dove viene configurato `BACKEND_URL`?
5. Quale endpoint dimostra che frontend e backend comunicano?
6. Che cosa cambia quando aggiorniamo l'immagine di una Container App?
7. Perché ACA introduce il concetto di revisione?
8. Dove leggiamo i log runtime?
9. Perché in ACA non usiamo `localhost` per collegare frontend e backend?
10. Quale evidenza dimostra che il deploy è completato correttamente?

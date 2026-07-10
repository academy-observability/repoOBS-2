# UD15 - Mini-attività
## Mappa FE/BE, immagini e ACR

Completa la mappa del flusso tecnico della UD15.

```text
GitHub repository
   |
   v
work/UD15
   |
   +--> frontend/  -> Dockerfile -> immagine frontend -> ACR
   |
   +--> backend/   -> Dockerfile -> immagine backend  -> ACR
```

## Domande

1. Perché frontend e backend hanno due Dockerfile separati?
2. Che differenza c'è tra monorepo e monolite?
3. Quale variabile permette al frontend di raggiungere il backend?
4. Perché usiamo una rete Docker locale nel test FE/BE?
5. Quali repository immagini devono comparire in ACR dopo la pipeline?
6. Perché `Build.BuildId` è utile come tag immagine?
7. Dove gira il build delle immagini nella pipeline?
8. Che cosa verifica lo stage `ValidateRepository`?
9. Che differenza c'è tra test locale FE/BE e pubblicazione immagini su ACR?
10. Perché in UD15 non facciamo ancora il deploy FE/BE nel cloud?

## Output richiesto

Scrivi una risposta breve per ciascun punto e aggiungi una mappa finale:

```text
frontend code -> frontend image -> ACR/frontend:<tag>
backend code  -> backend image  -> ACR/backend:<tag>
```

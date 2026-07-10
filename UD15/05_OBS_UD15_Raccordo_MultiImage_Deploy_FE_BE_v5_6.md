# UD15 - Raccordo finale
## Dalle immagini multiple al deploy FE/BE

In questa UD abbiamo costruito il passaggio da app singola a sistema composto da due servizi:

```text
frontend -> backend
```

Il risultato tecnico principale non è un'applicazione cloud già distribuita, ma due immagini pubblicate e verificabili:

```text
NOME_ACR.azurecr.io/frontend:<tag>
NOME_ACR.azurecr.io/backend:<tag>
```

## Cosa abbiamo consolidato

- frontend e backend sono servizi distinti;
- il monorepo non annulla la separazione dei servizi;
- ogni servizio ha un Dockerfile;
- ogni servizio produce una immagine;
- la pipeline multi-image pubblica entrambe le immagini in ACR;
- ACR diventa il punto di passaggio tra build e deploy.

## Perché questo passaggio è importante

Una pipeline che pubblica più immagini prepara scenari più realistici:

```text
codice FE/BE
-> build immagini
-> registry
-> deploy su una piattaforma runtime
-> osservazione del comportamento
```

Non è necessario anticipare qui tutta la piattaforma di deploy. La competenza che deve restare è questa:

```text
prima preparo immagini distinte e tracciabili;
poi potrò usarle in un rilascio più articolato.
```

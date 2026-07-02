# Configurazione UD08

Questa cartella contiene il file esempio `ud08.env.example`.

Procedura:

```bash
# Copia il file esempio in un file locale non versionato.
cp config/ud08.env.example config/ud08.env

# Apri il file e inserisci i valori reali del laboratorio.
nano config/ud08.env
```

Caricamento nel terminale:

```bash
# Esporta automaticamente le variabili definite nel file.
set -a
source config/ud08.env
set +a

# Verifica i valori caricati.
printf 'RG=%s\nLOCATION=%s\nLAW=%s\nWORKSPACE_ID=%s\n' "$RG" "$LOCATION" "$LAW" "$WORKSPACE_ID"
```

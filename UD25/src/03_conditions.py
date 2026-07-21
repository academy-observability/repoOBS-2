"""UD25 - Decisioni con if/elif/else."""

# MODIFICA GUIDATA - TASK 4
# Esegui lo script tre volte usando, nell'ordine: 503, 404 e 200.
status_code = 503

if status_code >= 500:
    print("Errore server: il servizio non ha completato correttamente la richiesta.")
elif status_code >= 400:
    print("Errore client: controllare la richiesta inviata.")
else:
    print("Richiesta completata senza errori HTTP 4xx/5xx.")

"""UD25 - Variabili, tipi e confronto numerico.

La prima esecuzione funziona perché duration_ms e threshold_ms sono numeri.
Nel Task 3 trasformeremo temporaneamente duration_ms in testo per osservare
un errore di tipo reale e poi correggerlo con float().
"""

service = "frontend"          # str: testo
status_code = 200             # int: numero intero

# MODIFICA GUIDATA - TASK 3
# Prima esecuzione: lascia 125.4 senza virgolette.
# Seconda esecuzione: sostituisci 125.4 con "125.4".
# Terza esecuzione: correggi usando float("125.4").
duration_ms = 125.4

threshold_ms = 120.0          # float: soglia numerica di prova
has_error = False             # bool: vero/falso

print("Servizio:", service)
print("Status code:", status_code)
print("Durata:", duration_ms, "ms")
print("Errore presente:", has_error)

print("Tipo di service:", type(service))
print("Tipo di status_code:", type(status_code))
print("Tipo di duration_ms:", type(duration_ms))
print("Tipo di threshold_ms:", type(threshold_ms))

# Questa riga rende visibile la differenza tra numero e testo.
print("Durata superiore a 120 ms:", duration_ms > threshold_ms)

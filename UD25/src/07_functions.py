"""UD25 - Funzioni semplici e riutilizzabili."""


def is_server_error(status_code):
    """Restituisce True quando lo status HTTP è 500 o superiore."""
    return status_code >= 500


def is_slow(duration_ms, threshold_ms):
    """Confronta una durata con una soglia fornita dal chiamante."""
    return duration_ms > threshold_ms


status_code = 503
duration_ms = 1450.0

print("Errore server:", is_server_error(status_code))
print("Più lenta di 1000 ms:", is_slow(duration_ms, 1000.0))

# MODIFICA GUIDATA - TASK 8
# Togli il carattere # dalla riga seguente e confronta i due risultati.
# print("Più lenta di 2000 ms:", is_slow(duration_ms, 2000.0))

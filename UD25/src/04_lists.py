"""UD25 - Liste e cicli for."""

durations_ms = [112.5, 128.0, 121.7, 940.2]

# MODIFICA GUIDATA - TASK 5
# Togli il carattere # dalla riga seguente, salva ed esegui di nuovo.
# durations_ms.append(1500.0)

print("Numero di durate:", len(durations_ms))

for duration_ms in durations_ms:
    print("Durata osservata:", duration_ms, "ms")

print("Durata massima:", max(durations_ms), "ms")

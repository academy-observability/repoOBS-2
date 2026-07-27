from __future__ import annotations

import sys

from common import base_url, build_client, chat, extract_model_names, model_name


def main() -> int:
    print(f"[INFO] endpoint: {base_url()}")
    print(f"[INFO] modello:  {model_name()}")
    print("[OK] endpoint configurato")

    try:
        client = build_client()
        print("[OK] package Python ollama disponibile")
    except RuntimeError as exc:
        print(f"[ERRORE] {exc}")
        return 1

    try:
        listed = client.list()
        names = extract_model_names(listed)
        print("[OK] API Ollama raggiungibile")
    except Exception as exc:
        print(f"[ERRORE] API non raggiungibile: {type(exc).__name__}: {exc}")
        print("[SUGGERIMENTO] Verificare 00A, OLLAMA_BASE_URL e curl Linux.")
        return 2

    selected = model_name()
    if selected not in names:
        print(f"[ERRORE] modello '{selected}' non trovato.")
        print("[INFO] modelli disponibili:")
        for name in names:
            print(f"  - {name}")
        print(f"[SUGGERIMENTO] Da WSL: ollama.exe pull {selected}")
        return 3
    print("[OK] modello disponibile")

    result = chat(
        "Rispondi soltanto con: PRECHECK_OK",
        prompt_name="precheck",
        client=client,
    )
    if not result.success:
        print(f"[ERRORE] inferenza fallita: {result.error}")
        return 4

    print("[OK] inferenza completata")
    print(f"[INFO] durata client: {result.client_duration_ms} ms")
    print(f"[INFO] token input:   {result.prompt_eval_count}")
    print(f"[INFO] token output:  {result.eval_count}")
    print(f"[INFO] risposta:      {result.text.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

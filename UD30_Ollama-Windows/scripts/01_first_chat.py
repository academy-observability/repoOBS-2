from common import chat, fill_prompt


def main() -> None:
    prompt = fill_prompt(
        "prompts/prompt_vincolato.txt",
        "evidence/incident_catalogo_guidato.md",
    )
    result = chat(prompt, prompt_name="prima_chat_vincolata")

    if not result.success:
        raise SystemExit(f"[ERRORE] {result.error}")

    print("=== RISPOSTA ===")
    print(result.text)
    print("\n=== TELEMETRIA ===")
    print(f"modello: {result.model}")
    print(f"durata client ms: {result.client_duration_ms}")
    print(f"durata totale ms: {result.total_duration_ms}")
    print(f"load duration ms: {result.load_duration_ms}")
    print(f"token input: {result.prompt_eval_count}")
    print(f"token output: {result.eval_count}")


if __name__ == "__main__":
    main()

from pathlib import Path

from common import chat, fill_prompt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"


def run(template: str, name: str):
    prompt = fill_prompt(template, "evidence/incident_catalogo_guidato.md")
    result = chat(prompt, prompt_name=name)
    text = result.text if result.success else f"ERRORE: {result.error}"
    (OUT / f"python_{name}.md").write_text(
        f"# Risposta {name}\n\n{text}\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    OUT.mkdir(exist_ok=True)
    results = [
        run("prompts/prompt_aperto.txt", "prompt_aperto"),
        run("prompts/prompt_vincolato.txt", "prompt_vincolato"),
    ]

    for result in results:
        status = "OK" if result.success else "ERRORE"
        print(
            f"[{status}] {result.prompt_name}: "
            f"{result.client_duration_ms} ms, "
            f"input={result.prompt_eval_count}, output={result.eval_count}"
        )
    print("[OK] Risposte salvate in outputs/")


if __name__ == "__main__":
    main()

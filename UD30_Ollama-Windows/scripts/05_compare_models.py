from __future__ import annotations

import csv
import os
from pathlib import Path

from common import build_client, chat, extract_model_names, fill_prompt

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "outputs" / "model_comparison.csv"


def main() -> None:
    requested = [
        item.strip()
        for item in os.getenv("OLLAMA_MODELS", "llama3.2:1b,gemma3:1b").split(",")
        if item.strip()
    ]
    client = build_client()
    available = set(extract_model_names(client.list()))
    selected = [m for m in requested if m in available]

    missing = [m for m in requested if m not in available]
    for model in missing:
        print(f"[SKIP] modello non disponibile: {model}")

    if len(selected) < 2:
        raise SystemExit("Servono almeno due modelli già scaricati per il confronto")

    prompt = fill_prompt(
        "prompts/prompt_vincolato.txt",
        "evidence/incident_catalogo_guidato.md",
    )

    rows = []
    for model in selected:
        result = chat(
            prompt,
            prompt_name="confronto_modelli",
            model=model,
            client=client,
        )
        row = result.row()
        row.pop("text", None)
        rows.append(row)
        print(
            f"[{model}] success={result.success}, "
            f"duration={result.client_duration_ms} ms, output={result.eval_count}"
        )

    OUTPUT.parent.mkdir(exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] confronto salvato: {OUTPUT}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path

from common import chat, fill_prompt

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "outputs" / "ollama_telemetry.csv"


def main() -> None:
    prompts = [
        ("aperto", fill_prompt("prompts/prompt_aperto.txt", "evidence/incident_catalogo_guidato.md")),
        ("vincolato_1", fill_prompt("prompts/prompt_vincolato.txt", "evidence/incident_catalogo_guidato.md")),
        ("vincolato_2", fill_prompt("prompts/prompt_vincolato.txt", "evidence/incident_catalogo_guidato.md")),
        ("breve", "Distingui in una frase un fatto osservato da un'ipotesi."),
    ]

    rows = []
    for run_id, (name, prompt) in enumerate(prompts, start=1):
        print(f"[INFO] esecuzione {run_id}/{len(prompts)}: {name}")
        result = chat(prompt, prompt_name=name)
        row = result.row()
        row.pop("text", None)  # il CSV tecnico non salva il contenuto del prompt/risposta
        row["run_id"] = run_id
        rows.append(row)

    OUTPUT.parent.mkdir(exist_ok=True)
    fields = [
        "run_id", "timestamp", "model", "prompt_name", "success",
        "client_duration_ms", "total_duration_ms", "load_duration_ms",
        "prompt_eval_count", "eval_count", "prompt_eval_duration_ms",
        "eval_duration_ms", "done_reason", "error",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] CSV creato: {OUTPUT}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "outputs" / "ollama_telemetry.csv"
FALLBACK = ROOT / "fallback" / "telemetry" / "ollama_telemetry_fallback.csv"


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        print(f"[INFO] {path} non trovato: uso fallback")
        path = FALLBACK

    data = pd.read_csv(path)
    data["success"] = data["success"].astype(str).str.lower().eq("true")
    ok = data[data["success"]].copy()

    print(f"Dataset: {path}")
    print(f"Esecuzioni: {len(data)}")
    print(f"Successi: {int(data['success'].sum())}")
    print(f"Fallimenti: {int((~data['success']).sum())}")

    if ok.empty:
        raise SystemExit("Nessuna esecuzione riuscita da analizzare")

    print("\n=== DURATE CLIENT ===")
    print(ok["client_duration_ms"].describe()[["min", "50%", "mean", "max"]].round(2))

    print("\n=== TOKEN ===")
    print(
        ok[["prompt_eval_count", "eval_count"]]
        .agg(["min", "median", "mean", "max"])
        .round(2)
    )

    if "load_duration_ms" in ok:
        print("\n=== LOAD DURATION ===")
        print(ok[["prompt_name", "load_duration_ms"]].to_string(index=False))

    valid = ok.dropna(subset=["eval_count", "eval_duration_ms"]).copy()
    valid = valid[valid["eval_duration_ms"] > 0]
    if not valid.empty:
        valid["output_tokens_per_second"] = (
            valid["eval_count"] / (valid["eval_duration_ms"] / 1000)
        )
        print("\n=== THROUGHPUT OUTPUT ===")
        print(
            valid[["prompt_name", "output_tokens_per_second"]]
            .round(2)
            .to_string(index=False)
        )

    print("\nNota: durate e token non misurano la correttezza semantica.")


if __name__ == "__main__":
    main()

"""Analizza con pandas il CSV di telemetria Ollama."""

from __future__ import annotations

from pathlib import Path
import pandas as pd

from common import BASE_DIR

RUNTIME_DATA = BASE_DIR / "runtime" / "ollama_runs.csv"
FALLBACK_DATA = BASE_DIR / "datasets" / "fallback_ollama_runs.csv"


def main() -> None:
    source = RUNTIME_DATA if RUNTIME_DATA.exists() else FALLBACK_DATA
    if not source.exists():
        raise SystemExit("Nessun CSV disponibile. Eseguire 03_collect_telemetry.py.")

    data = pd.read_csv(source)
    if data.empty:
        raise SystemExit(f"CSV vuoto: {source}")

    print(f"Dataset: {source}")
    print(f"Numero chiamate: {len(data)}")
    print("\nEsiti tecnici:")
    print(data["status"].value_counts(dropna=False).to_string())

    successful = data[data["status"] == "success"].copy()
    if successful.empty:
        print("\nNessuna chiamata riuscita: statistiche non disponibili.")
        return

    print("\nLatenza client:")
    print(f"  media: {successful['client_latency_ms'].mean():.2f} ms")
    print(f"  p95:   {successful['client_latency_ms'].quantile(0.95):.2f} ms")

    print("\nMedie per tipo di prompt:")
    by_prompt = successful.groupby("prompt_type")[
        ["client_latency_ms", "prompt_tokens", "output_tokens", "response_length"]
    ].mean().round(2)
    print(by_prompt.to_string())

    print("\nMedie per modello:")
    by_model = successful.groupby("model")[
        ["client_latency_ms", "prompt_tokens", "output_tokens"]
    ].mean().round(2)
    print(by_model.to_string())

    slowest = successful.loc[successful["client_latency_ms"].idxmax()]
    print("\nChiamata più lenta:")
    print(
        f"  {slowest['run_id']} | {slowest['model']} | "
        f"{slowest['client_latency_ms']:.2f} ms"
    )

    if "load_ms" in successful.columns:
        print("\nDurata di caricamento per chiamata:")
        print(successful[["run_id", "load_ms"]].to_string(index=False))


if __name__ == "__main__":
    main()

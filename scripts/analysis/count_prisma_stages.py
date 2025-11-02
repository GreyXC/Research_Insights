import json
import pandas as pd
from pathlib import Path

def count_prisma_stages():
    input_path = Path("data_sources/raw/cleaned_metadata.json")
    exclusion_path = Path("data_sources_raw/logs/prisma_exclusions.json")
    output_path = Path("data_sources_raw/logs/prisma_counts.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    df = pd.read_json(input_path)

    # Count entries tagged as mendeley_api
    identified = len(df[df["ingestion_source"] == "mendeley_api"])
    screened = identified

    # Load exclusion reasons and total
    excluded_total = 0
    if exclusion_path.exists():
        with exclusion_path.open("r", encoding="utf-8") as f:
            exclusion_data = json.load(f)
            if isinstance(exclusion_data, dict):
                excluded_total = sum(exclusion_data.values())
            elif isinstance(exclusion_data, int):
                excluded_total = exclusion_data

    assessed = screened - excluded_total
    included = assessed

    counts = {
        "records_identified": identified,
        "duplicates_removed": 0,
        "records_screened": screened,
        "records_excluded": excluded_total,
        "reports_assessed": assessed,
        "reports_excluded": 0,
        "studies_included": included
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)

    print("✅ PRISMA counts:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"\nCounts saved to: {output_path.resolve()}")

if __name__ == "__main__":
    count_prisma_stages()
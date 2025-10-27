import json
from pathlib import Path

def count_prisma_stages():
    counts = {
        "records_identified": 52,
        "duplicates_removed": 0,
        "records_screened": 52,
        "records_excluded": 9,
        "reports_assessed": 43,
        "reports_excluded": 0,
        "studies_included": 43
    }

    output_path = Path("data_sources_raw/logs/prisma_counts.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)

    print(f"Counts saved to: {output_path.resolve()}")

if __name__ == "__main__":
    count_prisma_stages()
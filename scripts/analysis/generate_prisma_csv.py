import json
import csv
from pathlib import Path

# Paths
COUNTS_PATH = Path("data_sources_raw/logs/prisma_counts.json")
CSV_PATH = Path("data_sources/raw/logs/prisma_flow.csv")

def generate_csv():
    if not COUNTS_PATH.exists():
        raise FileNotFoundError("Missing prisma_counts.json. Run count_prisma_stages.py first.")

    with COUNTS_PATH.open(encoding="utf-8") as f:
        c = json.load(f)

    rows = [
        {
            "data": "Records identified from: Mendeley Metadata",
            "node": "identification",
            "n": c.get("identified", 0),
            "note": ""
        },
        {
            "data": "Records removed before screening: duplicates",
            "node": "screening",
            "n": c.get("duplicates_removed", 0),
            "note": "Duplicate DOIs"
        },
        {
            "data": "Records screened",
            "node": "screening",
            "n": c.get("screened", 0),
            "note": ""
        },
        {
            "data": "Records excluded",
            "node": "screening",
            "n": c.get("excluded_screening", 0),
            "note": "Irrelevant or incomplete"
        },
        {
            "data": "Reports assessed for eligibility",
            "node": "eligibility",
            "n": c.get("eligibility", 0),
            "note": "Aligned with scope"
        },
        {
            "data": "Reports excluded",
            "node": "eligibility",
            "n": c.get("excluded_eligibility", 0),
            "note": "Out of scope"
        },
        {
            "data": "Studies included in synthesis",
            "node": "inclusion",
            "n": c.get("included", 0),
            "note": "relevant studies for analysis"
        }
    ]

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["data", "node", "n", "note"])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    generate_csv()
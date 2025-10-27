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
            "data": "Records identified from: Mendeley",
            "node": "identification",
            "box": "records_identified",
            "description": "Metadata records retrieved from Mendeley",
            "boxtext": f"{c['identified']} records identified",
            "tooltips": "Initial records retrieved from database",
            "url": ""
        },
        {
            "data": "Records removed before screening: duplicates",
            "node": "screening",
            "box": "duplicates_removed",
            "description": "Records removed due to duplicate DOIs",
            "boxtext": f"{c['duplicates_removed']} duplicates removed",
            "tooltips": "Removed based on duplicate identifiers",
            "url": ""
        },
        {
            "data": "Records screened",
            "node": "screening",
            "box": "records_screened",
            "description": "Records screened for relevance and completeness",
            "boxtext": f"{c['screened']} records screened",
            "tooltips": "Screening based on title, abstract, and year",
            "url": ""
        },
        {
            "data": "Records excluded",
            "node": "screening",
            "box": "records_excluded",
            "description": "Excluded due to missing or irrelevant metadata",
            "boxtext": f"{c['excluded_screening']} records excluded",
            "tooltips": "Missing abstract, title, or invalid year",
            "url": ""
        },
        {
            "data": "Reports assessed for eligibility",
            "node": "eligibility",
            "box": "full_text_articles",
            "description": "Remaining records assessed for full-text eligibility",
            "boxtext": f"{c['eligibility']} reports assessed",
            "tooltips": "Eligibility based on scope and availability",
            "url": ""
        },
        {
            "data": "Reports excluded",
            "node": "eligibility",
            "box": "reports_excluded",
            "description": "Excluded during full-text eligibility assessment",
            "boxtext": f"{c['excluded_eligibility']} reports excluded",
            "tooltips": "Out of scope or inaccessible",
            "url": ""
        },
        {
            "data": "Studies included in synthesis",
            "node": "inclusion",
            "box": "studies_included",
            "description": "Final records included in keyword synthesis",
            "boxtext": f"{c['included']} studies included",
            "tooltips": "Included in final analysis and visualisation",
            "url": ""
        }
    ]

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "data", "node", "box", "description", "boxtext", "tooltips", "url"
        ])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    generate_csv()
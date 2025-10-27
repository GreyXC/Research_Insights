import csv
import json
from pathlib import Path

def generate_csv():
    # Define input and output paths
    counts_path = Path("data_sources_raw/logs/prisma_counts.json")
    output_path = Path("data_sources_raw/logs/prisma_diagram.csv")

    # Check if the counts file exists
    if not counts_path.exists():
        raise FileNotFoundError("Missing prisma_counts.json. Run count_prisma_stages.py first.")

    # Load PRISMA counts
    with counts_path.open("r", encoding="utf-8") as f:
        counts = json.load(f)

    # Define rows in PRISMA format
    rows = [
        {
            "data": "records_identified",
            "node": "node7",
            "box": "box2",
            "description": "Records identified from: Mendeley",
            "boxtext": "Records identified",
            "tooltips": "Metadata records retrieved from Mendeley",
            "url": "NA",
            "n": counts.get("records_identified", 0)
        },
        {
            "data": "duplicates",
            "node": "node8",
            "box": "box3",
            "description": "Duplicate records removed",
            "boxtext": "Duplicate records",
            "tooltips": "Removed based on duplicate identifiers",
            "url": "NA",
            "n": counts.get("duplicates_removed", 0)
        },
        {
            "data": "records_screened",
            "node": "node9",
            "box": "box4",
            "description": "Records screened for relevance",
            "boxtext": "Records screened",
            "tooltips": "Screening based on title, abstract, and year",
            "url": "NA",
            "n": counts.get("records_screened", 0)
        },
        {
            "data": "records_excluded",
            "node": "node10",
            "box": "box5",
            "description": "Records excluded during screening",
            "boxtext": "Records excluded",
            "tooltips": "Excluded due to missing abstract, title, or invalid year",
            "url": "NA",
            "n": counts.get("records_excluded", 0)
        },
        {
            "data": "reports_assessed",
            "node": "node13",
            "box": "box8",
            "description": "Reports assessed for eligibility",
            "boxtext": "Reports assessed",
            "tooltips": "Eligibility based on scope and availability",
            "url": "NA",
            "n": counts.get("reports_assessed", 0)
        },
        {
            "data": "reports_excluded",
            "node": "node14",
            "box": "box9",
            "description": "Reports excluded during eligibility",
            "boxtext": "Reports excluded",
            "tooltips": "Out of scope or inaccessible",
            "url": "NA",
            "n": counts.get("reports_excluded", 0)
        },
        {
            "data": "studies_included",
            "node": "node15",
            "box": "box10",
            "description": "Studies included in synthesis",
            "boxtext": "Studies included",
            "tooltips": "Included in final analysis and visualisation",
            "url": "NA",
            "n": counts.get("studies_included", 0)
        }
    ]

    # Write to CSV
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["data", "node", "box", "description", "boxtext", "tooltips", "url", "n"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"PRISMA CSV saved to: {output_path.resolve()}")

# Entry point
if __name__ == "__main__":
    generate_csv()
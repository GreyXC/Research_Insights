import csv
import json
from pathlib import Path

def generate_csv():
    counts_path = Path("data_sources_raw/logs/prisma_counts.json")
    output_path = Path("data_sources_raw/logs/prisma_flow.csv")

    if not counts_path.exists():
        raise FileNotFoundError("Missing prisma_counts.json. Run count_prisma_stages.py first.")

    with counts_path.open("r", encoding="utf-8") as f:
        counts = json.load(f)

    def row(data, node, box, description, boxtext, tooltips, url, key=None):
        return {
            "data": data,
            "node": node,
            "box": box,
            "description": description,
            "boxtext": boxtext,
            "tooltips": tooltips,
            "url": url,
            "n": counts.get(key, 0) if key else 0
        }

    rows = [
        # Structural anchors
        row("NA", "node4", "prevstud", "Grey title box; Previous studies", "Previous studies", "Grey title box; Previous studies", "prevstud.html"),
        row("NA", "node6", "newstud", "Yellow title box; Identification of new studies via databases and registers", "Identification of new studies via databases and registers", "Yellow title box; Identification of new studies via databases and registers", "newstud.html"),
        row("NA", "node16", "othstud", "Grey title box; Identification of new studies via other methods", "Identification of new studies via other methods", "Grey title box; Identification of new studies via other methods", "othstud.html"),

        # Blue section boxes
        row("identification", "node1", "identification", "Blue identification box", "Identification", "Blue identification box", "identification.html"),
        row("screening", "node2", "screening", "Blue screening box", "Screening", "Blue screening box", "screening.html"),
        row("included", "node3", "included", "Blue included box", "Included", "Blue included box", "included.html"),

        # Identification
        row("database_results", "node7", "box2", "Records identified from: Databases", "Databases", "Records identified from: Databases and Registers", "database_results.html", "records_identified"),
        row("database_specific_results", "NA", "box2", "Records identified from: specific databases", "Specific Databases", "NA", "database_results.html"),
        row("register_results", "NA", "box2", "Records identified from: Registers", "Registers", "NA", "NA"),
        row("register_specific_results", "NA", "box2", "Records identified from: specific registers", "Specific Registers", "NA", "database_results.html"),

        # Other sources
        row("website_results", "node17", "box11", "Records identified from: Websites", "Websites", "Records identified from: Websites, Organisations and Citation Searching", "website_results.html"),
        row("organisation_results", "NA", "box11", "Records identified from: Organisations", "Organisations", "NA", "NA"),
        row("citations_results", "NA", "box11", "Records identified from: Citation searching", "Citation searching", "NA", "NA"),

        # Screening
        row("duplicates", "node8", "box3", "Duplicate records", "Duplicate records", "Duplicate records", "duplicates.html", "duplicates_removed"),
        row("excluded_automatic", "NA", "box3", "Records marked as ineligible by automation tools", "Records marked as ineligible by automation tools", "NA", "NA"),
        row("excluded_other", "NA", "box3", "Records removed for other reasons", "Records removed for other reasons", "NA", "NA"),
        row("records_screened", "node9", "box4", "Records screened (databases and registers)", "Records screened", "Records screened (databases and registers)", "records_screened.html", "records_screened"),
        row("records_excluded", "node10", "box5", "Records excluded (databases and registers)", "Records excluded", "Records excluded (databases and registers)", "records_excluded.html", "records_excluded"),

        # Eligibility
        row("dbr_sought_reports", "node11", "box6", "Reports sought for retrieval (databases and registers)", "Reports sought for retrieval", "Reports sought for retrieval (databases and registers)", "dbr_sought_reports.html"),
        row("dbr_notretrieved_reports", "node12", "box7", "Reports not retrieved (databases and registers)", "Reports not retrieved", "Reports not retrieved (databases and registers)", "dbr_notretrieved_reports.html"),
        row("other_sought_reports", "node18", "box12", "Reports sought for retrieval (other)", "Reports sought for retrieval", "Reports sought for retrieval (other)", "other_sought_reports.html"),
        row("other_notretrieved_reports", "node19", "box13", "Reports not retrieved (other)", "Reports not retrieved", "Reports not retrieved (other)", "other_notretrieved_reports.html"),
        row("dbr_assessed", "node13", "box8", "Reports assessed for eligibility (databases and registers)", "Reports assessed for eligibility", "Reports assessed for eligibility (databases and registers)", "dbr_assessed.html", "reports_assessed"),
        row("dbr_excluded", "node14", "box9", "Reports excluded (databases and registers): [separate reasons and numbers using ; e.g. Reason1, xxx; Reason2, xxx; Reason3, xxx]", "Reports excluded", "Reports excluded (databases and registers)", "dbrexcludedrecords.html", "reports_excluded"),
        row("other_assessed", "node20", "box14", "Reports assessed for eligibility (other)", "Reports assessed for eligibility", "Reports assessed for eligibility (other)", "other_assessed.html"),
        row("other_excluded", "node21", "box15", "Reports excluded (other): [separate reasons and numbers using ; e.g. Reason1, xxx; Reason2, xxx; Reason3, xxx]", "Reports excluded", "Reports excluded (other)", "other_excluded.html"),

        # Inclusion
        row("new_studies", "node15", "box10", "New studies included in review", "New studies included in review", "New studies included in review", "new_studies.html", "studies_included"),
        row("new_reports", "NA", "box10", "Reports of new included studies", "Reports of new included studies", "NA", "NA"),
        row("total_studies", "node22", "box16", "Total studies included in review", "Total studies included in review", "Total studies included in review", "total_studies.html", "studies_included"),
        row("total_reports", "NA", "box16", "Reports of total included studies", "Total reports", "NA", "NA", "studies_included"),

        # Previous studies
        row("previous_studies", "node5", "box1", "Studies included in previous version of review", "Studies included in previous version of review", "Studies included in previous version of review", "previous_studies.html"),
        row("previous_reports", "NA", "box1", "Reports of studies included in previous version of review", "Reports of studies included in previous version of review", "NA", "previous_reports.html")
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["data", "node", "box", "description", "boxtext", "tooltips", "url", "n"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ PRISMA2020-compliant CSV saved to: {output_path.resolve()}")

if __name__ == "__main__":
    generate_csv()
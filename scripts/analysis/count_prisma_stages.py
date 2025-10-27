import json
from pathlib import Path

# Paths
METADATA_PATH = Path("data_sources/raw/mendeley_metadata.json")
CLEANED_PATH = Path("data_sources/raw/cleaned_metadata.json")
DECISIONS_PATH = Path("data_sources_raw/logs/prisma_decisions.jsonl")
COUNTS_PATH = Path("data_sources_raw/logs/prisma_counts.json")

def count_prisma_stages():
    # Load metadata
    identified = 0
    if METADATA_PATH.exists():
        with METADATA_PATH.open(encoding="utf-8") as f:
            identified = len(json.load(f))

    # Load cleaned metadata
    included = 0
    if CLEANED_PATH.exists():
        with CLEANED_PATH.open(encoding="utf-8") as f:
            included = len(json.load(f))

    # Load PRISMA decisions
    excluded_screening = 0
    excluded_eligibility = 0
    duplicates_removed = 0

    if DECISIONS_PATH.exists():
        with DECISIONS_PATH.open(encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("stage") == "screening" and entry.get("decision") == "exclude_irrelevant":
                    excluded_screening += 1
                elif entry.get("stage") == "eligibility" and entry.get("decision").startswith("exclude"):
                    excluded_eligibility += 1
                elif entry.get("stage") == "screening" and entry.get("decision") == "exclude_duplicate":
                    duplicates_removed += 1

    # Derived counts
    screened = max(0, identified - duplicates_removed)
    eligibility = max(0, screened - excluded_screening)
    included = max(0, eligibility - excluded_eligibility)

    # Save counts
    COUNTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COUNTS_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "identified": identified,
            "duplicates_removed": duplicates_removed,
            "screened": screened,
            "excluded_screening": excluded_screening,
            "eligibility": eligibility,
            "excluded_eligibility": excluded_eligibility,
            "included": included
        }, f, indent=2)

    print("PRISMA counts updated.")

if __name__ == "__main__":
    count_prisma_stages()
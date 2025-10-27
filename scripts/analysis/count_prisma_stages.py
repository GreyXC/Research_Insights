import json
from pathlib import Path

# Paths
DECISIONS_PATH = Path("data_sources_raw/logs/prisma_decisions.jsonl")
METADATA_PATH = Path("data_sources/raw/cleaned_metadata.json")
COUNTS_PATH = Path("data_sources_raw/logs/prisma_counts.json")

def count_stage_decisions(stage, decision_type):
    if not DECISIONS_PATH.exists():
        return 0
    with DECISIONS_PATH.open(encoding="utf-8") as f:
        return sum(
            1 for line in f
            if (entry := json.loads(line))["stage"] == stage and entry["decision"] == decision_type
        )

def count_loaded():
    if not METADATA_PATH.exists():
        return 0
    with METADATA_PATH.open(encoding="utf-8") as f:
        return len(json.load(f))

def update_counts():
    counts = {
        "identified": count_loaded(),
        "duplicates_removed": count_stage_decisions("screening", "exclude_duplicate"),
        "excluded_screening": count_stage_decisions("screening", "exclude_irrelevant"),
        "excluded_eligibility": count_stage_decisions("eligibility", "exclude_scope"),
    }
    counts["screened"] = counts["identified"] - counts["duplicates_removed"]
    counts["eligibility"] = counts["screened"] - counts["excluded_screening"]
    counts["included"] = counts["eligibility"] - counts["excluded_eligibility"]

    COUNTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COUNTS_PATH.open("w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)

if __name__ == "__main__":
    update_counts()
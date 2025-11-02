import pandas as pd
import json
from pathlib import Path
from ..analysis.log_prisma_decision import log_decision

def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans a DataFrame by:
    - Dropping rows with missing or short abstracts
    - Stripping whitespace from 'title' and 'abstract'
    - Replacing semicolons with commas in 'tags'
    - Extracting 4-digit years from 'year'
    Also logs PRISMA screening exclusions and returns exclusion reasons.
    """
    df = df.copy()
    valid_rows = []
    exclusion_reasons = {}

    def is_valid_record(row):
        abstract = row.get("abstract", "")
        title = row.get("title", "")
        year = row.get("year", "")

        # Normalize abstract
        if isinstance(abstract, list):
            abstract = " ".join(map(str, abstract))
        if not isinstance(abstract, str):
            abstract = str(abstract)
        abstract = abstract.strip()

        # Normalize title
        if not isinstance(title, str):
            title = str(title)
        title = title.strip()

        # Extract year
        year_str = str(year)
        year_match = pd.Series(year_str).str.extract(r"(\d{4})")[0]
        valid_year = year_match.iloc[0] if not year_match.isna().iloc[0] else None

        # Apply filters
        if abstract == "" or len(abstract) < 30:
            return False, "Missing or short abstract"
        if title == "":
            return False, "Missing title"
        if valid_year is None:
            return False, "Invalid or missing year"
        return True, None

    for idx, row in df.iterrows():
        keep, reason = is_valid_record(row)
        if keep:
            row_dict = row.to_dict()
            valid_rows.append(row_dict)
        else:
            log_decision(record_id=str(idx), stage="screening", decision="exclude_irrelevant", reason=reason)
            exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1

    df_cleaned = pd.DataFrame(valid_rows)

    # Final cleanup
    if "abstract" in df_cleaned.columns:
        df_cleaned["abstract"] = df_cleaned["abstract"].astype(str).str.strip()
    if "title" in df_cleaned.columns:
        df_cleaned["title"] = df_cleaned["title"].astype(str).str.strip()
    if "tags" in df_cleaned.columns:
        df_cleaned["tags"] = df_cleaned["tags"].str.replace(";", ",", regex=False).str.strip()
    if "year" in df_cleaned.columns:
        df_cleaned["year"] = df_cleaned["year"].astype(str).str.extract(r"(\d{4})")

    return df_cleaned, exclusion_reasons

theme_map_name = "logistics_review"

if __name__ == "__main__":
    input_path = Path("data_sources/raw/mendeley_metadata.json")
    output_path = Path("data_sources/raw/cleaned_metadata.json")
    exclusion_path = Path("data_sources_raw/logs/prisma_exclusions.json")

    if input_path.exists():
        df = pd.read_json(input_path)
        df["ingestion_source"] = "mendeley_api"

        cleaned, exclusion_reasons = clean_dataframe(df)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cleaned.to_json(output_path, orient="records", indent=2)
        print(f"Cleaned data saved to {output_path}")

        exclusion_path.parent.mkdir(parents=True, exist_ok=True)
        with exclusion_path.open("w", encoding="utf-8") as f:
            json.dump(exclusion_reasons, f, indent=2)
        print(f"Exclusion summary saved to {exclusion_path}")
    else:
        print(f"Input file not found: {input_path}")
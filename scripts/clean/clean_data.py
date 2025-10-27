import pandas as pd
from pathlib import Path
from ..analysis.log_prisma_decision import log_decision

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a DataFrame by:
    - Dropping rows with missing abstracts
    - Stripping whitespace from 'title' and 'abstract'
    - Replacing semicolons with commas in 'tags'
    - Extracting 4-digit years from 'year'
    Also logs PRISMA screening exclusions.
    """
    df = df.copy()
    initial_ids = df.index.astype(str)

    # Drop missing abstracts
    if "abstract" in df.columns:
        missing_abstracts = df[df["abstract"].isna()]
        for idx in missing_abstracts.index:
            log_decision(record_id=str(idx), stage="screening", decision="exclude_irrelevant", reason="Missing abstract")
        df = df.dropna(subset=["abstract"])
        df["abstract"] = df["abstract"].str.strip()

    # Strip title
    if "title" in df.columns:
        df["title"] = df["title"].str.strip()
        empty_titles = df[df["title"].isna() | (df["title"].str.strip() == "")]
        for idx in empty_titles.index:
            log_decision(record_id=str(idx), stage="screening", decision="exclude_irrelevant", reason="Missing title")

    # Clean tags
    if "tags" in df.columns:
        df["tags"] = df["tags"].str.replace(";", ",", regex=False).str.strip()

    # Extract 4-digit years
    if "year" in df.columns:
        df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")
        invalid_years = df[df["year"].isna()]
        for idx in invalid_years.index:
            log_decision(record_id=str(idx), stage="screening", decision="exclude_irrelevant", reason="Invalid or missing year")

    return df

# Optional: theme map name for downstream use
theme_map_name = "logistics_review"

# Optional CLI/test entry point
if __name__ == "__main__":
    input_path = Path("data_sources/raw/mendeley_metadata.json")
    output_path = Path("data_sources/raw/cleaned_metadata.json")

    if input_path.exists():
        df = pd.read_json(input_path)
        cleaned = clean_dataframe(df)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cleaned.to_json(output_path, orient="records", indent=2)
        print(f"Cleaned data saved to {output_path}")
    else:
        print(f"Input file not found: {input_path}")
def clean_dataframe(df):
    """
    Cleans a DataFrame by:
    - Dropping rows with missing abstracts
    - Stripping whitespace from 'title' and 'abstract'
    - Replacing semicolons with commas in 'tags'
    - Extracting 4-digit years from 'year'
    """
    df = df.copy()
    if "abstract" in df.columns:
        df = df.dropna(subset=["abstract"])
        df["abstract"] = df["abstract"].str.strip()
    if "title" in df.columns:
        df["title"] = df["title"].str.strip()
    if "tags" in df.columns:
        df["tags"] = df["tags"].str.replace(";", ",").str.strip()
    if "year" in df.columns:
        df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")
    return df

theme_map_name = "logistics_review"  # or another valid map name

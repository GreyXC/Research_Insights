def clean(df):
    df = df.copy()
    df["title"] = df["title"].str.strip()
    df["abstract"] = df["abstract"].str.strip()
    df["tags"] = df["tags"].str.replace(";", ",").str.strip()
    df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")
    return df

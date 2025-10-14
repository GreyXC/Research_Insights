def clean_dataframe(df):
    df = df.dropna(subset=["abstract"])
    df["abstract"] = df["abstract"].str.strip()
    return df

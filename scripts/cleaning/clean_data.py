def clean(df):
    df = df.dropna()
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

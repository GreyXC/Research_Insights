import os
import rispy
import pandas as pd

def load_ris(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"RIS file not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        entries = rispy.load(f)

    df = pd.DataFrame(entries)
    df = df.rename(columns={
        "title": "title",
        "abstract": "abstract",
        "authors": "authors",
        "publication_year": "year"
    })

    columns_to_keep = ["title", "abstract", "authors", "year"]
    df = df[[col for col in columns_to_keep if col in df.columns]]

    return df

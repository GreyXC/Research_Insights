import pandas as pd
from scripts.load.load_ris import load_ris
from scripts.clean.clean_data import clean_dataframe
from scripts.extract.extract_keywords import extract_keywords
from scripts.visualize.plot_keywords import plot_keywords

def run_pipeline():
    print("Loading RIS data...")
    df_raw = load_ris("data_sources/raw/mendeley_export.ris")
    df_clean = clean_dataframe(df_raw)
    print(f"Loaded {len(df_clean)} cleaned abstracts.")

    print("\nExtracting keywords...")
    keywords = extract_keywords(df_clean, "abstract")
    print(f"Top keywords: {[kw[0] for kw in keywords]}")

    print("\nGenerating keyword frequency bar chart...")
    plot_keywords(keywords, config_dir="config/theme_maps")

if __name__ == "__main__":
    run_pipeline()

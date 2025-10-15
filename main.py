import pandas as pd
from scripts.load.load_ris import load_ris
from scripts.clean.clean_data import clean_dataframe
from scripts.extract.extract_keywords import extract_keywords
from scripts.visualize.plot_keywords import plot_keywords
from scripts.analysis.analyze_insights import extract_themes
from scripts.visualize.plot_themes import plot_theme_clusters

def run_pipeline():
    print("Loading RIS data...")
    df_raw = load_ris("data_sources/raw/mendeley_export.ris")
    df_clean = clean_dataframe(df_raw)
    print(f"Loaded {len(df_clean)} cleaned abstracts.")

    print("\nExtracting keywords...")
    keywords = extract_keywords(df_clean, "abstract")
    print("Top Keywords:", keywords)

    theme_map_name = "logistics_review"  # Set your default theme map here
    print(f"\nGrouping keywords using theme map: {theme_map_name}")
    themes = extract_themes(df_clean, map_name=theme_map_name)
    for theme, words in themes.items():
        print(f"\n{theme.upper()}:")
        for word, count in words:
            print(f"  {word} ({count})")

    print("\nGenerating clustered keyword frequency plot...")
    plot_theme_clusters(themes)  

if __name__ == "__main__":
    run_pipeline()

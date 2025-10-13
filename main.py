from scripts.extraction.parse_ris import parse_ris
from scripts.cleaning.clean_data import clean
from scripts.analysis.analyze_insights import extract_keywords, extract_themes
from scripts.visualize.plot_themes import plot_theme_clusters 

def run_pipeline():
    theme_map_name = "logistics_review"  # Change to emissions_policy, ai_design, etc.

    print("Parsing RIS file...")
    df = parse_ris("data_sources/raw/mendeley_export.ris")
    print("Loaded records:", df.shape)

    print("Cleaning data...")
    df_clean = clean(df)

    print("Extracting top keywords from abstracts...")
    keywords = extract_keywords(df_clean, "abstract")
    print("Top Keywords:", keywords)

    print(f"\nGrouping keywords using theme map: {theme_map_name}")
    themes = extract_themes(df_clean, map_name=theme_map_name)
    for theme, words in themes.items():
        print(f"\n{theme.upper()}:")
        for word, count in words:
            print(f"  {word} ({count})")

    print("\nGenerating clustered keyword frequency plot...")
    plot_theme_clusters(themes)  # ✅ Trigger plot

if __name__ == "__main__":
    run_pipeline()

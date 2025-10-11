from scripts.extraction.extract_sources import load_local_csv
from scripts.cleaning.clean_data import clean
from scripts.analysis.analyze_insights import extract_keywords

def run_pipeline():
    df = load_local_csv("data_sources/raw/source.csv")
    df_clean = clean(df)
    keywords = extract_keywords(df_clean, "abstract")
    print("Top Keywords:", keywords)

if __name__ == "__main__":
    run_pipeline()

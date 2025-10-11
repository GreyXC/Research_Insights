from scripts.extraction.parse_ris import parse_ris
from scripts.cleaning.clean_data import clean
from scripts.analysis.analyze_insights import extract_keywords

def run_pipeline():
    print("Parsing RIS file...")
    df = parse_ris("data_sources/raw/mendeley_export.ris")
    print("Loaded records:", df.shape)

    print("Cleaning data...")
    df_clean = clean(df)

    print("Extracting keywords...")
    keywords = extract_keywords(df_clean, "abstract")

    print("Top Keywords:", keywords)

if __name__ == "__main__":
    run_pipeline()

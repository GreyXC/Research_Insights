import json
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load metadata
with open("data_sources/raw/mendeley_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Setup
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    if not text:
        return []
    tokens = re.findall(r"\b\w+\b", text.lower())
    return [stemmer.stem(t) for t in tokens if t not in stop_words]

# Normalize entries
normalized = []
for entry in metadata:
    title = entry.get("title", "").strip()
    abstract = entry.get("abstract", "")
    keywords = entry.get("keywords") or []

    abstract_tokens = clean_text(abstract)
    keyword_tokens = [stemmer.stem(k.lower()) for k in keywords if isinstance(k, str)]

    normalized.append({
        "title": title,
        "year": entry.get("year"),
        "keywords": list(set(abstract_tokens + keyword_tokens)),
    })

print(f"Normalized {len(normalized)} entries")
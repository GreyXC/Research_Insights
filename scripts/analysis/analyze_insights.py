import re
import json
from collections import Counter, defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_keywords(df, column="abstract", top_n=20):
    stop_words = set(stopwords.words("english"))
    all_text = " ".join(df[column].dropna().tolist()).lower()
    cleaned_text = re.sub(r"[^\w\s]", "", all_text)
    words = word_tokenize(cleaned_text, preserve_line=True)  #  Fixes punkt_tab bug
    filtered = [w for w in words if w not in stop_words and len(w) > 2 and not w.isnumeric()]
    freq = Counter(filtered)
    return [word for word, count in freq.most_common(top_n)]

def extract_themes(df, column="abstract", map_name="logistics_review"):
    path = f"config/theme_maps/{map_name}.json"
    with open(path, encoding="utf-8") as f:
        theme_map = json.load(f)

    stop_words = set(stopwords.words("english"))
    all_text = " ".join(df[column].dropna().tolist()).lower()
    cleaned_text = re.sub(r"[^\w\s]", "", all_text)
    words = word_tokenize(cleaned_text, preserve_line=True)  #  Fixes punkt_tab bug
    filtered = [w for w in words if w not in stop_words and len(w) > 2 and not w.isnumeric()]
    freq = Counter(filtered)

    themes = defaultdict(list)
    for theme, keywords in theme_map.items():
        for kw in keywords:
            if kw in freq:
                themes[theme].append((kw, freq[kw]))

    return {theme: sorted(words, key=lambda x: x[1], reverse=True) for theme, words in themes.items()}

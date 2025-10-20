import re
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Ensure stopwords are available
try:
    _ = stopwords.words("english")
except LookupError:
    import nltk
    nltk.download("stopwords")

def extract_keywords_from_abstracts(df, column="abstract"):
    stop_words = set(stopwords.words("english")) | ENGLISH_STOP_WORDS
    keyword_lists = []

    for text in df[column]:
        if not isinstance(text, str):
            keyword_lists.append([])
            continue

        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        filtered = [word for word in tokens if word not in stop_words]
        keyword_lists.append(filtered)

    return keyword_lists

def cluster_keywords(df, column="abstract", n_clusters=6):
    # Extract keywords from abstract text
    keyword_lists = extract_keywords_from_abstracts(df, column=column)

    # Use pre-tokenized input and bypass string preprocessing
    vectorizer = CountVectorizer(
        analyzer='word',
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        lowercase=True
    )
    X = vectorizer.fit_transform(keyword_lists)
    terms = vectorizer.get_feature_names_out()

    # Cluster documents
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    # Global term frequency from matrix
    term_freq = X.sum(axis=0).A1
    term_freq_map = dict(zip(terms, term_freq))

    # Assign keywords to clusters based on document labels
    cluster_terms = defaultdict(list)
    for idx, label in enumerate(labels):
        for term in keyword_lists[idx]:
            cluster_terms[label].append(term)

    # Aggregate keyword frequencies per cluster using global term frequency
    clustered = {}
    for label, terms in cluster_terms.items():
        unique_terms = set(terms)
        ranked = sorted(unique_terms, key=lambda t: term_freq_map.get(t, 0), reverse=True)
        clustered[f"Cluster {label+1}"] = [(term, int(term_freq_map.get(term, 0))) for term in ranked[:15]]

    return clustered
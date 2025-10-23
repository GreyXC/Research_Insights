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

def cluster_keywords(df, column="word_list", n_clusters=6, return_tokens=False):
    stop_words = set(stopwords.words("english")) | ENGLISH_STOP_WORDS

    # Use pre-cleaned token lists from df[column]
    keyword_lists = df[column].tolist()

    # Filter stopwords
    filtered_lists = [
        [word for word in tokens if word not in stop_words]
        for tokens in keyword_lists
    ]

    # Use pre-tokenized input and bypass string preprocessing
    vectorizer = CountVectorizer(
        analyzer='word',
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        lowercase=False
    )
    X = vectorizer.fit_transform(filtered_lists)
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
        for term in filtered_lists[idx]:
            cluster_terms[label].append(term)

    # Aggregate keyword frequencies per cluster using global term frequency
    clustered = {}
    for label, terms in cluster_terms.items():
        unique_terms = set(terms)
        ranked = sorted(unique_terms, key=lambda t: term_freq_map.get(t, 0), reverse=True)
        clustered[f"Cluster {label+1}"] = [(term, int(term_freq_map.get(term, 0))) for term in ranked[:15]]

    if return_tokens:
        return clustered, filtered_lists
    return clustered
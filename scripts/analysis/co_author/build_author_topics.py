import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import defaultdict, Counter

# Lazy model loader for sentence-transformers to avoid importing heavy
# dependencies at module import time unless the author embeddings are used.
_sbert_model = None


def build_author_embeddings(parsed_entries):
    author_texts = defaultdict(list)
    for entry in parsed_entries:
        authors = entry.get("authors", [])
        abstract = entry.get("abstract", "")
        for author in authors:
            if abstract:
                author_texts[author].append(abstract)
    # Lazy-load the SentenceTransformer model on first use
    global _sbert_model
    if _sbert_model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception:
            raise
        _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = {}
    for author, texts in author_texts.items():
        joined = " ".join(texts)
        embeddings[author] = _sbert_model.encode(joined)
    return embeddings

 

def cluster_author_embeddings(embeddings, n_clusters=2):
    X = np.array(list(embeddings.values()))
    kmeans = KMeans(n_clusters=n_clusters, random_state=15000)
    labels = kmeans.fit_predict(X)
    return dict(zip(embeddings.keys(), labels))

 

def label_clusters_by_keywords(parsed_entries, cluster_map, top_k=5):
    cluster_texts = defaultdict(list)
    for entry in parsed_entries:
        authors = entry.get("authors", [])
        abstract = entry.get("abstract", "")
        for author in authors:
            cluster_id = cluster_map.get(author)
            if cluster_id is not None and abstract:
                cluster_texts[cluster_id].extend(abstract.lower().split())

    cluster_labels = {}
    for cluster_id, words in cluster_texts.items():
        common = [w for w, _ in Counter(words).most_common(500) if len(w) > 4]
        label = ", ".join(common[:top_k])
        cluster_labels[cluster_id] = label
    return cluster_labels

 

def project_embeddings_pca(embeddings, n_components=2):
    authors = list(embeddings.keys())
    X = np.array([embeddings[a] for a in authors])
    coords = PCA(n_components=n_components).fit_transform(X)
    return dict(zip(authors, coords))
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_fields(entry):
    title = entry.get('title', '')
    abstract = entry.get('abstract', '')
    keywords = ' '.join(entry.get('keywords', []))
    return f"{title} {abstract} {keywords}".strip()

def build_author_embeddings(entries):
    author_texts = defaultdict(list)
    for entry in entries:
        text = extract_text_fields(entry)
        if not text:
            continue
        for author in entry.get('authors', []):
            author_texts[author].append(text)

    author_embeddings = {}
    for author, texts in author_texts.items():
        vectors = model.encode(texts)
        author_embeddings[author] = np.mean(vectors, axis=0)

    return author_embeddings

def cluster_author_embeddings(embeddings, n_clusters=6):
    authors = list(embeddings.keys())
    X = np.array([embeddings[a] for a in authors])
    labels = KMeans(n_clusters=n_clusters, random_state=42).fit_predict(X)
    return dict(zip(authors, labels))

def label_clusters_by_keywords(entries, semantic_labels, top_k=2):
    cluster_texts = defaultdict(list)

    for entry in entries:
        text = extract_text_fields(entry)
        if not text:
            continue
        for author in entry.get('authors', []):
            cluster = semantic_labels.get(author)
            if cluster is not None:
                cluster_texts[cluster].append(text)

    cluster_labels = {}
    for cluster, texts in cluster_texts.items():
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(texts)
        scores = X.sum(axis=0).A1
        terms = vectorizer.get_feature_names_out()
        top_terms = [terms[i] for i in scores.argsort()[::-1][:top_k]]
        cluster_labels[cluster] = ', '.join(top_terms)

    return cluster_labels
from typing import Any, cast
from sklearn.feature_extraction.text import CountVectorizer


def extract_keywords(df, text_column: str = "abstract", top_n: int = 10):
    """Return the top `top_n` keywords (word, count) from `text_column` in `df`.

    Uses `CountVectorizer` to build a document-term matrix. Casts the sparse
    matrix to `Any` before calling `.sum(...).A1` to satisfy static analyzers.
    """
    vectorizer = CountVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(df[text_column].fillna(""))
    X_any = cast(Any, X)
    word_counts = X_any.sum(axis=0).A1
    keywords = list(zip(vectorizer.get_feature_names_out(), word_counts))
    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords[:top_n]

from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(df, column="abstract", top_n=10):
    corpus = df[column].dropna().tolist()
    vectorizer = CountVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(corpus)
    word_counts = X.sum(axis=0).A1
    keywords = sorted(
        zip(vectorizer.get_feature_names_out(), word_counts),
        key=lambda x: x[1],
        reverse=True
    )
    return [kw for kw, _ in keywords[:top_n]]

from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(df, text_column="abstract", top_n=20):
    vectorizer = CountVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(df[text_column].fillna(""))
    word_counts = X.sum(axis=0).A1
    keywords = list(zip(vectorizer.get_feature_names_out(), word_counts))
    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords[:top_n]

from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(df, text_column="abstract", top_n=10):
    vectorizer = CountVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(df[text_column].fillna(""))
    word_counts = X.sum(axis=0).A1
    keywords = list(zip(vectorizer.get_feature_names_out(), word_counts))
    keywords.sort(key=lambda x: x[1], reverse=True)
    return keywords[:top_n]

from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(df, column):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df[column])
    keywords = vectorizer.get_feature_names_out()
    return keywords[:20]

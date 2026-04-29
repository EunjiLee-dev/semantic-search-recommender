from sklearn.feature_extraction.text import TfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TFIDFSearch:
    def __init__(self, texts):
        self.vectorizer = TfidVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query, top_k=5):
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        top_indices = sims.argsort()[::-1][:top_k]

        return top_indices

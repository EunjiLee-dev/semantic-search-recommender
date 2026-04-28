import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# load data
embeddings = np.load("data/embeddings/poi_embeddings.npy")
metadata = np.load("data/embeddings/metadata.npy", allow_pickle=True)


# compare similarity and return top 5
def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=5):
    query_vec = model.encode(query)
    
    scores = []
    for i, emb in enumerate(embeddings):
        score = cosine_similarity(query_vec, emb)
        scores.append((i, score))

    scores.sort(key=lambda x:x[1], reverse=True)
    top_results = scores[:top_k]

    results = []
    for idx, score in top_results:
        item = metadata[idx]
        results.append({
            "name": item["name"],
            "categories": item["categories"],
            "score": float(score)
        })

    return results
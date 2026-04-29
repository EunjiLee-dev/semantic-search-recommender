import numpy as np
from sentence_transformers import SentenceTransformer
from app.services.ranking import price_score, distance_score, final_score, parse_query_intent

model = SentenceTransformer("all-MiniLM-L6-v2")

USER_LAT = 47.37
USER_LON = 8.54


# load data
embeddings = np.load("data/embeddings/poi_embeddings.npy")
metadata = np.load("data/embeddings/metadata.npy", allow_pickle=True)


# compare similarity and return top 5
def cosine_similarity(a,b):
    return np.dot(a, b)

def search(query, top_k=5):
    query_vec = model.encode(query, normalize_embeddings=True)

    intent = parse_query_intent(query)
    has_intent = any(intent.values())
    
    scores = []

    for i, emb in enumerate(embeddings):
        semantic = cosine_similarity(query_vec, emb)
        item = metadata[i]

        price = price_score(query, item.get("price_level"))
        distance = distance_score(
            USER_LAT, USER_LON,
            item.get("latitude"),
            item.get("longitude")
        )

        total = final_score(
            semantic,
            price,
            distance,
            has_intent
        )

        scores.append((i, total))

    scores.sort(key=lambda x:x[1], reverse=True)
    top_results = scores[:top_k]

    results = []
    for idx, score in top_results:
        item = metadata[idx]
        results.append({
            "name": item["name"],
            "categories": item["categories"],
            "score": float(score),
            "price_level": item.get("price_level"),
        })

    return results
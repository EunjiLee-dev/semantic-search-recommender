import numpy as np
import math
from sentence_transformers import SentenceTransformer
from app.services.ranking import (
    price_score, 
    distance_score, 
    final_score, 
    parse_query_intent, 
    apply_hard_filters,
    build_explanation
)

model = SentenceTransformer("all-MiniLM-L6-v2")

USER_LAT = 47.37
USER_LON = 8.54


# load data
embeddings = np.load("data/embeddings/poi_embeddings.npy")
metadata = np.load("data/embeddings/metadata.npy", allow_pickle=True)


# compare similarity and return top 5
def safe_float(x):
    if x is None:
        return 0.0
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return 0.0
    return float(x)

def cosine_similarity(a,b):
    return np.dot(a, b)

def search(query, top_k=5):
    query_vec = model.encode(query, normalize_embeddings=True)

    intent = parse_query_intent(query)
    print(intent) 
    has_intent = any(intent.values())

    filtered_indices = apply_hard_filters(metadata, intent)
    
    scores = []

    for i in filtered_indices:
        item = metadata[i]
        emb = embeddings[i]

        semantic = cosine_similarity(query_vec, emb)
        
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
    for i, score in top_results:
        item = metadata[i]
        results.append({
            "name": item["name"],
            "categories": item["categories"],
            "score": safe_float(score),
            "breakdown": {
                "semantic": safe_float(semantic),
                "price": safe_float(price),
                "distance": safe_float(distance),
            },
            "explanation": build_explanation(
                semantic,
                price,
                distance,
            ),
            "price_level": safe_float(item.get("price_level")),
            "wifi": item.get("WiFi"),
            "reservation": item.get("RestaurantsReservations"),
            "parking": item.get("BusinessParking"),
            "delivery": item.get("RestaurantsDelivery"),
        })

    return results

search("sushi with wifi")
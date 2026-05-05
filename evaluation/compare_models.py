import pandas as pd
import json
from app.services.search import search as search_sbert
from baseline.tfidf import TFIDFSearch
from evaluation.metrics import relevance_score, intent_match, price_match


# load data
df = pd.read_csv("data/processed/poi_clean.csv")

texts = df["text"].tolist()
tfidf = TFIDFSearch(texts)


def safe_bool(x):
    if x is None:
        return None
    return bool(x)

def safe_value(x):
  return None if pd.isna(x) else x


def search_tfidf(query):
    tfidf_indices = tfidf.search(query, top_k=5)
    tfidf_results = []

    for idx in tfidf_indices:
        row = df.iloc[idx]

        tfidf_results.append({
            "name": row["name"],
            "categories": row["categories"],
            "price_level": safe_value(row.get("price_level")),
            "wifi": safe_bool(row.get("WiFi")),
            "parking": safe_bool(row.get("BusinessParking")),
            "delivery": safe_bool(row.get("RestaurantsDelivery")),
            "reservation": safe_bool(row.get("RestaurantsReservations"))
        })

    return tfidf_results


def evaluate():
    with open("evaluation/test_queries.json") as f:
        queries = json.load(f)

    results_summary = []

    for query in queries:
        q = query["query"]

        tfidf_results = search_tfidf(q)[:5]
        sbert_results = search_sbert(q)[:5]

        tfidf_score = evaluate_results(tfidf_results, query)
        sbert_score = evaluate_results(sbert_results, query)

        results_summary.append({
            "query": q,
            "tfidf_score": tfidf_score,
            "sbert_score": sbert_score,
            "tfidf_results": tfidf_results,
            "sbert_results": sbert_results
        })

    return results_summary


def evaluate_results(results, query):
    scores = []
    for res in results:
        score = 0

        if relevance_score(res, query.get("expected_categories", [])):
            score += 1
        
        if intent_match(res, query.get("must_have", [])):
            score += 1

        if price_match(res, query.get("price_level_max")):
            score += 1

        scores.append(score)

    return sum(scores) / len(scores) if scores else 0


results_summary = evaluate()


with open("evaluation/results.json", "w") as f:
    json.dump(results_summary, f, indent=2)

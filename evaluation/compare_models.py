import pandas as pd
import json
from app.services.search import search as sbert_search
from baseline.tfidf import TFIDFSearch


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


# compare with test queries
OUTPUT_PATH = "evaluation/results.json"
results_all = []

queries = [
    "cheap sushi with parking",
    "luxury pizza and wine",
    "hamburger with wifi",
    "coffee and bread"
]

for query in queries:
    # TF-IDF
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
        })
    
    # SBERT
    sbert_results_raw = sbert_search(query)

    sbert_results = []
    for r in sbert_results_raw:
        name = r["name"]

        match_row = df[df["name"] == name].iloc[0] if len(df[df["name"] == name]) > 0 else None

        sbert_results.append({
            "name": r["name"],
            "categories": r["categories"],
            "score": r["score"],
            "price_level": safe_value(match_row.get("price_level")) if match_row is not None else None,
            "wifi": safe_bool(match_row.get("WiFi")) if match_row is not None else None,
            "parking": safe_bool(match_row.get("BusinessParking")) if match_row is not None else None,
        })

    # store
    results_all.append({
        "query": query,
        "tfidf": tfidf_results,
        "sbert": sbert_results
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results_all, f, indent=2, ensure_ascii=False)

print(f"Saved evaluation results to {OUTPUT_PATH}")
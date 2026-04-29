from app.services.search import search as sbert_search
from baseline.tfidf import TFIDFSearch
import pandas as pd
import json


# load data
df = pd.read_csv("data/processed/poi_clean.csv")

texts = df["text"].tolist()
tfidf = TFIDFSearch(texts)


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
        tfidf_results.append({
            "name": df.iloc[idx]["name"],
            "categories": df.iloc[idx]["categories"]
        })
    
    # SBERT
    sbert_results_raw = sbert_search(query)

    sbert_results = []
    for r in sbert_results_raw:
        sbert_results.append({
            "name": r["name"],
            "categories": r["categories"],
            "score": r["score"]
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
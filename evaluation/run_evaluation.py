import json
from app.search import search
from evaluation.metrics import relevance_score, intent_match, price_match


def evaluate():
    with open("evaluation/test_queries.json") as f:
        queries = json.load(f)

    results_summary = []

    for query in queries:
        results = search(query["query"])[:5]

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

        avg_score = sum(scores) / len(scores) if scores else 0

        results_summary.append({
            "query":query["query"],
            "avg_score": avg_score
        })

    return results_summary

results_summary = evaluate()


with open("evaluation/results.json", "w") as f:
    json.dump(results_summary, f, indent=2)
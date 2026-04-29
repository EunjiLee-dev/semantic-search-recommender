from app.services.search import search

queries = [
    "cheap sushi",
    "expensive sushi",
    "not expensive sushi",
]

for q in queries:
    print("=" * 50)
    print(f"QUERY: {q}")

    results = search(q, top_k=5)

    for r in results:
        print(r)
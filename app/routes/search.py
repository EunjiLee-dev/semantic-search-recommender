from fastapi import APIRouter, Query
from app.services.search import search

router = APIRouter()

@router.get("/search")
def search_endpoint(q: str = Query(...), top_k: int = 5):
    results = search(q, top_k)
    return {
        "query": q,
        "results": results
    }
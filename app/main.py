from fastapi import FastAPI
from app.routes import search

app = FastAPI(title="Semantic Search API")

app.include_router(search.router)

@app.get("/")
def root():
    return {"message": "Semantic Search API is running."}
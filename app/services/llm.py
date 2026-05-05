import requests

def generate_answer(query, context):
    prompt = f"""
You are a recommendation explanation system.

Strict rules:
- Use ONLY provided information
- DO NOT infer missing features
- DO NOT add new facts (e.g., parking size, fees, authenticity)
- DO NOT use marketing words (e.g., best, authentic, perfect)

Query: {query}
Candidates: {context}
"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"qwen2.5:3b",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2
        }
    )

    return response.json()["response"]
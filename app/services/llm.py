import requests


def generate_answer(query, context):
    prompt = f"""
You are a recommendation assistant.
User query: {query}
Relevant places: {context}
Give me a helpful recommendation.
"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"phi3:mini",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
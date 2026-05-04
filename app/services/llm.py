import requests


def generate_answer(query, context):
    prompt = f"""
You are a recommendation assistant.
Q: {query}
Context: {context}
Answer briefly in 2-3 sentences.
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
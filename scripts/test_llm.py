from app.services.llm import generate_answer

query = "cheap sushi"
context = "Sushi Park | Restaurants | price:2"

result = generate_answer(query, context)

print(result)
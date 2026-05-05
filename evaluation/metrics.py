def relevance_score(result, expected_categories):
    return any(cat.lower() in result["categories"].lower()
               for cat in expected_categories)

def intent_match(result, must_have):
    return all(result.get(f) == True for f in must_have)

def price_match(result, max_price):
    price = result.get("price_level")
    
    if max_price is None:
        return True

    if price is None:
        return False
    
    return price <= max_price
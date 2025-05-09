import re

class ProductSearchAI:
    def process_query(self, query):
        # Example: basic extraction
        price_match = re.search(r'(\d+)[\s-]*to[\s-]*(\d+)', query)
        category = None
        if "phone" in query.lower():
            category = "mobile phones"
        elif "laptop" in query.lower():
            category = "laptops"

        filters = {}
        if category:
            filters["category"] = category
        if price_match:
            filters["price_range"] = f"{price_match.group(1)}-{price_match.group(2)}"

        return {
            "search_term": query,
            "filters": filters
        }

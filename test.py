from api_handler import fetch_amazon_products
from recommender import RecommendationEngine

def run_tests():
    print("Fetching Mock Data...")
    data = fetch_amazon_products("laptop")
    print(f"Got {len(data)} items.\n")
    
    print("Testing ML Recommendation Engine...")
    engine = RecommendationEngine()
    
    user_req = "I want a very fast gaming laptop. Don't care about battery."
    ranked = engine.rank_products(user_req, data)
    
    print("Top Recommended Match:")
    if ranked:
        top = ranked[0]
        print(f"Title: {top['title']}")
        print(f"Match percentage: {top['match_percentage']}%")
        print(f"Reasoning/Description: {top['description']}")
    print("\nTest Complete!")

if __name__ == "__main__":
    run_tests()

import requests
import urllib.parse

def fetch_amazon_products(query, api_key=None):
    """
    Fetches product data from the RapidAPI Real-Time Amazon Data API.
    If no API key or request fails, returns a robust fallback dataset for demonstration.
    """
    if api_key:
        encoded_query = urllib.parse.quote(query)
        url = f"https://real-time-amazon-data.p.rapidapi.com/search?query={encoded_query}&page=1&country=IN&sort_by=RELEVANCE&product_condition=NEW&is_prime=false&deals_and_discounts=NONE"

        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                products = data.get('data', {}).get('products', [])
                # Return mapped Data
                return [
                    {
                        "title": p.get("product_title"),
                        "price": p.get("product_price"),
                        "rating": float(p.get("product_star_rating")) if p.get("product_star_rating") else 0.0,
                        "reviews": int(p.get("product_num_ratings")) if p.get("product_num_ratings") else 0,
                        "url": p.get("product_url"),
                        "image": p.get("product_photo"),
                        "description": f"{p.get('product_title')} with competitive pricing and excellent features." # Fallback desc
                    } for p in products if p.get("product_title")
                ]
            else:
                print(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")
            
    # Fallback Data if API fails or no Key is provided
    print("Using Fallback Mock Data...")
    return get_fallback_data(query)

def get_fallback_data(query):
    """
    Provides fallback data for a smooth user experience.
    """
    q = query.lower()
    if 'laptop' in q or 'computer' in q:
        return [
             {"title": "Dell XPS 13 OLED Laptop - 13.4-inch FHD+, Intel Core i7, 16GB RAM, 512GB SSD", "price": "₹1,09,990.00", "rating": 4.5, "reviews": 1204, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80", "description": "High performance ultrabook for business and travel. Brilliant color and thin frame construction."},
             {"title": "HP Pavilion 15.6 Laptop, AMD Ryzen 5, 8GB RAM, 256GB SSD", "price": "₹45,990.00", "rating": 4.3, "reviews": 540, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1588872657578-7dfd134d1d29?w=500&q=80", "description": "Budget friendly everyday computer with long battery life. Suitable for students and casual use."},
             {"title": "Razer Blade 15 Gaming Laptop: NVIDIA GeForce RTX 3070 Ti - 12th Gen Intel Core i7", "price": "₹2,10,000.00", "rating": 4.8, "reviews": 340, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&q=80", "description": "Powerful gaming rig with superior cooling and high framerates for competitive play."},
             {"title": "LG Gram 17Z90P Laptop 17 IPS Ultra-Lightweight", "price": "₹95,000.00", "rating": 4.6, "reviews": 850, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80", "description": "Incredibly light with a massive 17-inch screen. The battery lasts over 12 hours."}
        ]
    elif 'mouse' in q or 'mice' in q:
        return [
             {"title": "Logitech MX Master 3S - Wireless Performance Mouse", "price": "₹8,999.00", "rating": 4.8, "reviews": 12050, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80", "description": "Ultimate precision mouse for productivity, featuring a MagSpeed scroll wheel and ergonomic design."},
             {"title": "Razer DeathAdder V3 Pro Wireless Gaming Mouse", "price": "₹12,499.00", "rating": 4.7, "reviews": 2100, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1615663245857-ac1eeb536fcb?w=500&q=80", "description": "Ultra-lightweight competitive gaming mouse with extreme precision."}
        ]
    elif 'phone' in q or 'vivo' in q or 'mobile' in q:
        return [
             {"title": "Vivo X90 Pro 5G Factory Unlocked Smartphone", "price": "₹74,999.00", "rating": 4.7, "reviews": 890, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&q=80", "description": "Flagship device with an incredible Zeiss camera array, Dedicated V2 chip and ultra-fast charging."},
             {"title": "Vivo V27 5G Mobile Phone 256GB", "price": "₹32,999.00", "rating": 4.5, "reviews": 1200, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80", "description": "Aura light portrait system with a gorgeous 3D curved screen and responsive processor for everyday use."},
             {"title": "Samsung Galaxy S23 Ultra, 256GB", "price": "₹1,04,999.00", "rating": 4.8, "reviews": 15000, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&q=80", "description": "Ultimate productivity phone featuring the S-Pen, dynamic AMOLED display, and snapdragon 8 gen 2."}
        ]
    else:
        # Generic products
        return [
             {"title": "Bose QuietComfort 45 Bluetooth Wireless Noise Cancelling Headphones", "price": "₹22,900.00", "rating": 4.7, "reviews": 15000, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80", "description": "Industry leading noise cancellation, clear sound, and ultimate comfort for travel."},
             {"title": "Kindle Paperwhite (8 GB) – Now with a 6.8 display", "price": "₹14,999.00", "rating": 4.8, "reviews": 25000, "url": "https://amazon.in", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&q=80", "description": "Built for reading with a glare-free display and weeks of battery life."}
        ]

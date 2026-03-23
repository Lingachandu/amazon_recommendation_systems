import streamlit as st
import pandas as pd
from api_handler import fetch_amazon_products
from recommender import RecommendationEngine

st.set_page_config(page_title="AI Amazon Recommender", page_icon="🛍️", layout="wide")

# Inject Custom Styling
st.markdown("""
<style>
    /* Global Theme Adjustments */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    h1, h2, h3 {
        color: #e2e8f0 !important;
    }
    
    /* Custom Product Card */
    .product-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6);
        border-color: #3b82f6;
    }
    
    .card-layout {
        display: flex;
        gap: 24px;
        align-items: flex-start;
    }
    .card-image-col {
        flex: 0 0 28%;
        max-width: 28%;
    }
    .card-content-col {
        flex: 1;
    }
    
    @media (max-width: 768px) {
        .card-layout {
            flex-direction: column;
        }
        .card-image-col {
            flex: 0 0 100%;
            max-width: 100%;
            margin-bottom: 20px;
            text-align: center;
        }
        .card-image-col img {
            width: 60% !important;
            max-width: 300px;
        }
    }
    
    .product-title {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 14px;
        line-height: 1.4;
    }
    .product-title-number {
        color: #3b82f6;
        font-size: 24px;
    }
    
    .product-stats {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        background-color: #0f172a;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid #1e293b;
    }
    .stat-item {
        display: flex;
        align-items: center;
        font-size: 15px;
        color: #cbd5e1;
    }
    .match-score {
        color: #10b981;
        font-weight: 800;
        font-size: 16px;
        background: rgba(16, 185, 129, 0.1);
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .stat-value {
        font-weight: 600;
        color: #f8fafc;
        margin-left: 6px;
    }
    
    .product-desc {
        color: #94a3b8;
        font-size: 15px;
        line-height: 1.6;
        border-left: 4px solid #3b82f6;
        padding-left: 14px;
        margin-bottom: 20px;
        background: rgba(59, 130, 246, 0.05);
        border-radius: 0 8px 8px 0;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .amazon-btn {
        display: inline-block;
        background-color: #f59e0b;
        color: #1e293b !important;
        font-weight: 700;
        padding: 10px 24px;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.2);
    }
    .amazon-btn:hover {
        background-color: #fbbf24;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(245, 158, 11, 0.3);
    }
    
    .product-card a {
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ ML & NLP Amazon Product Recommender")
st.markdown("""
This app searches Amazon and uses **Machine Learning (TF-IDF Cosine Similarity)** and **Natural Language Processing (Sentiment Analysis)** to find the exact product that matches your specific text requirements!
""")

st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("RapidAPI Key (Optional)", value="13a4cc7603msha67369f6a5df090p15876cjsnc26ffa21c485", type="password", help="Leave blank to use the built-in fallback dataset.")
if not api_key:
    st.sidebar.warning("No API Key detected. Using robust offline Mock Data for demonstration.")

st.subheader("1. Your Information")
user_name = st.text_input("What is your name?", value="Guest")

st.subheader("2. General Search")
search_query = st.text_input("What broad category are you looking for? (e.g., Laptop, Mouse, Headphones)", value="Laptop")

st.subheader("3. Sorting & Layout")
sort_preference = st.selectbox("How would you like your results sorted?", 
                                ["Match Score (Default ML logic)", "Rating (Highest First)", "Number of Reviews (Most Popular)"])

st.subheader("4. Specific Requirements (NLP Matching)")
user_reqs = st.text_area("Describe exactly what you need in detail. The ML engine will match this text against product descriptions.", 
                         value="I need a powerful device for gaming and creative work. Needs a dedicated GPU and fast processor.")

if st.button("🔍 Find My Perfect Product", type="primary"):
    if search_query and user_reqs:
        with st.spinner("Fetching data and running Machine Learning text analysis..."):
            
            # 1. Fetch Data
            products_data = fetch_amazon_products(search_query, api_key=api_key if api_key else None)
            
            if not products_data:
                st.error("No data found or API limit reached. Try clearing the API key to use offline data.")
            else:
                # 2. Run ML Recommendation
                engine = RecommendationEngine()
                
                # Apply the user's selected sorting filter
                ranked_data = engine.rank_products(user_reqs, products_data, sort_by=sort_preference)
                
                ranked_products = ranked_data.get("products", [])
                metrics = ranked_data.get("metrics", {})
                
                # 3. Display Results
                st.success(f"Hello {user_name}! Successfully analyzed {len(ranked_products)} products using TF-IDF & Cosine Similarity.")
                
                # Display Metrics Dashboard
                if metrics:
                    st.markdown("### 📊 NLP Analysis Metrics")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Average Match Score", f"{metrics.get('avg_match_score', 0)}%")
                    m2.metric("Highest Similarity", f"{metrics.get('max_nlp_similarity', 0)}%")
                    m3.metric("Avg Sentiment Polarity", f"{metrics.get('avg_sentiment', 0)}")
                    st.divider()
                
                st.markdown(f"### 🏆 Top 5 Matches for {user_name} (Sorted by {sort_preference.split(' ')[0]})")
                
                # Display up to 5 results cleanly in custom HTML format
                for idx, prod in enumerate(ranked_products[:5]):
                    image_tag = f'<img src="{prod.get("image")}" style="width: 100%; border-radius: 8px; object-fit: contain; background: white; padding: 10px;" alt="Product Image">' if prod.get("image") else ''
                    url_tag = f'<a href="{prod.get("url")}" target="_blank" class="amazon-btn">🛒 View on Amazon</a>' if prod.get("url") else ''
                    
                    card_html = f"""
                    <div class="product-card">
                        <div class="card-layout">
                            <div class="card-image-col">
                                {image_tag}
                            </div>
                            <div class="card-content-col">
                                <div class="product-title">
                                    <span class="product-title-number">#{idx+1}:</span> {prod.get('title')}
                                </div>
                                <div class="product-stats">
                                    <div class="stat-item match-score">
                                        🎯 Match Score: {prod.get('match_percentage', 0)}%
                                    </div>
                                    <div class="stat-item">
                                        💰 Price: <span class="stat-value">{prod.get('price')}</span>
                                    </div>
                                    <div class="stat-item">
                                        ⭐ Rating: <span class="stat-value">{prod.get('rating')} ({prod.get('reviews')} reviews)</span>
                                    </div>
                                </div>
                                <div class="product-desc">
                                    <b>💡 Why it matches:</b><br>{prod.get('description')}
                                </div>
                                {url_tag}
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.warning("Please enter both a search query and specific requirements.")

st.markdown("---")
st.markdown("*Built with Streamlit, Scikit-Learn, and TextBlob.*")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import pandas as pd
import numpy as np

class RecommendationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def analyze_sentiment(self, text):
        """
        Uses TextBlob to assign a sentiment polarity to the product text.
        Positive sentiment slightly boosts the score later.
        """
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
        
    def rank_products(self, user_requirements, products_data, sort_by="Match Score"):
        """
        Takes specific user textual requirements and scores the products.
        Uses NLP for description matching via Cosine Similarity and ML algorithms.
        """
        if not products_data:
            return []

        df = pd.DataFrame(products_data)
        
        # We will build a text corpus from product title + description for robust matching
        corpus = (df['title'] + " " + df['description']).tolist()
        
        # Add the User's specific requirement as the FIRST item in the corpus
        corpus.insert(0, user_requirements)
        
        try:
            # TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Compare the first index (user req) against the rest (products)
            cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Incorporate sentiment & rating into the final score
            final_scores = []
            
            for idx, row in df.iterrows():
                text_sim = cosine_similarities[idx]
                sentiment = self.analyze_sentiment(row['title'] + " " + row['description'])
                
                # Normalize rating to 0-1 scale (Assume max is 5)
                norm_rating = row['rating'] / 5.0
                
                # Weighted Final Score formula
                # 60% textual match, 25% general rating, 15% positive sentiment framing
                score = (0.60 * text_sim) + (0.25 * norm_rating) + (0.15 * max(0, sentiment))
                
                # Adding some slight penalty if the text sim is completely 0 
                # to avoid pushing highly rated but irrelevant things up
                if text_sim < 0.05:
                     score = score * 0.1 

                final_scores.append(score)

            # Attach scores and sort
            # Attach scores and generate percentage
            df['match_score'] = final_scores
            df['match_percentage'] = (df['match_score'] * 100).round(1)
            
            # Calculate Evaluation Metrics before sorting
            avg_match_score = df['match_percentage'].mean().round(1)
            # The similarities array index 0 is the user prompt compared to itself (1.0). 
            # So, we check similarities from index 1 onwards to find the max product match.
            max_sim_score = (cosine_similarities.max() * 100).round(1) if len(cosine_similarities) > 0 else 0.0
            avg_sentiment = np.mean([self.analyze_sentiment(r['title'] + " " + r['description']) for _, r in df.iterrows()]).round(2)
            df['match_score'] = final_scores
            df['match_percentage'] = (df['match_score'] * 100).round(1)
            
            # Apply Selected Sorting Logic
            if sort_by == "Rating (Highest First)":
                df = df.sort_values(by=['rating', 'match_score'], ascending=[False, False]).reset_index(drop=True)
            elif sort_by == "Number of Reviews (Most Popular)":
                df = df.sort_values(by=['reviews', 'match_score'], ascending=[False, False]).reset_index(drop=True)
            else:
                # Default ML Match Score Sort
                df = df.sort_values(by='match_score', ascending=False).reset_index(drop=True)
            
            # Format nicely as dicts
            # Multiply match_score by 100 for percentage representation
            df['match_percentage'] = (df['match_score'] * 100).round(1)
            
            return {
                "products": df.to_dict('records'),
                "metrics": {
                    "avg_match_score": avg_match_score,
                    "max_nlp_similarity": max_sim_score,
                    "avg_sentiment": avg_sentiment
                }
            }
            
        except Exception as e:
            print(f"Error in recommendation engine: {e}")
            return {"products": products_data, "metrics": {}} # Return unsorted on error


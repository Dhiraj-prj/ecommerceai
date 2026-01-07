"""
Pure ML Recommendation Engine
- Builds user interest profiles from behavior
- TF-IDF vectorization
- Cosine similarity matching
- Returns top product recommendations
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommenderEngine:
    def __init__(self):
        """Initialize TF-IDF vectorizer with optimal settings"""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,        # Top 1000 words
            stop_words='english',     # Remove common words
            min_df=2,                 # Word must appear in 2+ products
            max_df=0.8,               # Ignore words in 80%+ products
            ngram_range=(1, 2)        # Single words + 2-word phrases
        )
        self.is_fitted = False
        self.vocabulary = None
    
    def fit(self, product_contexts):
        """Train vectorizer on all product contexts (vocabulary + IDF scores)"""
        if not product_contexts:
            raise ValueError("No product contexts provided!")
        
        self.vectorizer.fit(product_contexts)
        self.is_fitted = True
        self.vocabulary = self.vectorizer.get_feature_names_out()
        print(f"✅ Fitted with vocabulary size: {len(self.vocabulary)} words")
    
    def build_interest_profile(self, behaviors):
        """
        Convert user behaviors → interest text with proper weighting
        
        Args:
            behaviors: List of dicts:
                {'action': 'search', 'searchquery': 'wireless headphones'}
                {'action': 'view', 'productcontext': 'wireless bluetooth gym'}
        
        Returns:
            Single text string representing user interests
        """
        if not behaviors:
            return ""
        
        interest_parts = []
        
        # 🔹 SEARCHES (Weight 3x) - Most explicit user intent
        searches = [b for b in behaviors if b['action'] == 'search']
        for search in searches:
            interest_parts.extend([search['searchquery']] * 3)
        
        # 🔹 CLICKS (Weight 2x) - Strong engagement signal
        clicks = [b for b in behaviors if b['action'] == 'click']
        for click in clicks:
            interest_parts.extend([click['productcontext']] * 2)
        
        # 🔹 VIEWS (Weight 1x) - Passive interest
        views = [b for b in behaviors if b['action'] == 'view']
        for view in views:
            interest_parts.append(view['productcontext'])
        
        # Combine all with spaces
        interest_text = " ".join(interest_parts).strip()
        print(f"📝 Built interest profile ({len(interest_parts)} signals):")
        print(f"   '{interest_text[:100]}...'")
        
        return interest_text
    
    def get_recommendations(self, user_behaviors, product_contexts, top_n=5):
        """
        COMPLETE RECOMMENDATION PIPELINE
        
        Args:
            user_behaviors: List of user behavior dicts
            product_contexts: List of ALL active product contexts
            top_n: Number of recommendations
            
        Returns:
            List of (product_index, similarity_score, product_context)
        """
        if not self.is_fitted:
            raise ValueError("Must call fit() first with product contexts!")
        
        if not user_behaviors:
            print("⚠️  No user behaviors - returning empty recommendations")
            return []
        
        # Step 1: Build user interest profile
        interest_text = self.build_interest_profile(user_behaviors)
        if not interest_text:
            return []
        
        # Step 2: Vectorize user interest
        user_vector = self.vectorizer.transform([interest_text])
        
        # Step 3: Vectorize all products
        product_vectors = self.vectorizer.transform(product_contexts)
        
        # Step 4: Calculate cosine similarities
        similarities = cosine_similarity(user_vector, product_vectors)[0]
        
        # Step 5: Get top N recommendations
        top_indices = np.argsort(-similarities)[:top_n]
        
        recommendations = []
        for idx in top_indices:
            score = similarities[idx]
            if score > 0.1:  # Minimum relevance threshold
                recommendations.append({
                    'product_index': int(idx),
                    'similarity_score': float(score),
                    'match_percentage': round(float(score) * 100, 1),
                    'product_context': product_contexts[idx]
                })
        
        print(f"🎯 Found {len(recommendations)} recommendations (max {top_n})")
        return recommendations
    
    def explain_recommendation(self, user_behaviors, product_context, top_words=5):
        """Explain WHY this product was recommended"""
        interest_text = self.build_interest_profile(user_behaviors)
        user_vector = self.vectorizer.transform([interest_text])
        product_vector = self.vectorizer.transform([product_context])
        
        # Get top matching words
        feature_names = self.vocabulary
        user_scores = user_vector.toarray()[0]
        product_scores = product_vector.toarray()[0]
        
        matches = []
        for i, (user_score, prod_score) in enumerate(zip(user_scores, product_scores)):
            if user_score > 0.1 and prod_score > 0.1:
                matches.append((feature_names[i], user_score, prod_score))
        
        matches.sort(key=lambda x: x[1] * x[2], reverse=True)
        top_matches = matches[:top_words]
        
        explanation = f"Matches on: {', '.join([m[0] for m in top_matches])}"
        return explanation

# 🧪 TEST FUNCTION (Run this file directly to test!)
if __name__ == "__main__":
    print("🧠 Testing ML Engine...")
    
    # Sample products (rich contexts!)
    products = [
        "wireless bluetooth headphones gym bass sports running fitness",
        "noise cancelling earbuds office commute travel bluetooth wireless",
        "winter jacket fleece outdoor hiking cold weather waterproof",
        "wireless earbuds bass boost gym workout fitness sports audio",
        "gaming headphones rgb lights bass boost esports competitive",
        "running shoes lightweight trail running breathable marathon"
    ]
    
    # Sample user behaviors
    user_behaviors = [
        {'action': 'search', 'searchquery': 'wireless headphones'},
        {'action': 'search', 'searchquery': 'gym headphones'},
        {'action': 'click', 'productcontext': products[0]},
        {'action': 'view', 'productcontext': products[3]}
    ]
    
    # Create and test engine
    engine = RecommenderEngine()
    engine.fit(products)
    
    # Get recommendations
    recs = engine.get_recommendations(user_behaviors, products, top_n=3)
    
    print("\n🎉 RECOMMENDATIONS:")
    for i, rec in enumerate(recs, 1):
        print(f"{i}. Product #{rec['product_index']}")
        print(f"   Score: {rec['match_percentage']}%")
        print(f"   Context: {rec['product_context'][:60]}...")
        print()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import get_user_behaviors, get_products
from ml.recommender import RecommenderEngine
from schemas import Recommendation
from models import Product, UserBehavior
from typing import List
import uuid

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# Global ML Engine (singleton pattern)
recommendation_engine = RecommenderEngine()

@router.get("/", response_model=List[Recommendation])
async def get_user_recommendations(
    user_id: str = "demo_user_1",
    top_n: int = 5,
    db: Session = Depends(get_db)
):
    """
    🔥 MAIN RECOMMENDATIONS ENDPOINT
    Returns personalized recommendations based on user behavior history
    """
    
    # Step 1: Get user behaviors from database
    behaviors = get_user_behaviors(db, user_id)
    if not behaviors:
        raise HTTPException(status_code=404, detail="No behavior history. Browse/search first!")
    
    # Step 2: Get active products
    active_products = get_products(db)
    if not active_products:
        raise HTTPException(status_code=404, detail="No active products available!")
    
    product_contexts = [p.productcontext for p in active_products]
    
    # Step 3: Fit ML engine if needed
    if not recommendation_engine.is_fitted:
        recommendation_engine.fit(product_contexts)
    
    # Step 4: Convert DB behaviors to ML format
    user_behaviors = []
    for behavior in behaviors:
        if behavior.action == 'search':
            user_behaviors.append({
                'action': 'search',
                'searchquery': behavior.searchquery
            })
        else:  # view or click
            product = db.query(Product).filter(Product.id == behavior.productid).first()
            if product:
                user_behaviors.append({
                    'action': behavior.action,
                    'productcontext': product.productcontext
                })
    
    # Step 5: Generate recommendations!
    recs = recommendation_engine.get_recommendations(user_behaviors, product_contexts, top_n)
    
    # Step 6: Format response with product details
    recommendations = []
    for rec in recs:
        product = active_products[rec['product_index']]
        recommendations.append({
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'similarity_score': rec['similarity_score'],
            'match_percentage': rec['match_percentage'],
            'explanation': recommendation_engine.explain_recommendation(
                user_behaviors, product.productcontext
            )
        })
    
    return recommendations[:top_n]

@router.get("/debug/{user_id}")
async def debug_recommendations(user_id: str, db: Session = Depends(get_db)):
    """Debug endpoint - shows raw data"""
    behaviors = get_user_behaviors(db, user_id)
    products = get_products(db)
    
    return {
        "user_id": user_id,
        "behavior_count": len(behaviors),
        "product_count": len(products),
        "behaviors": [
            {
                "action": b.action,
                "searchquery": b.searchquery,
                "product_id": b.productid,
                "timestamp": b.timestamp
            }
            for b in behaviors[-10:]  # Last 10
        ]
    }

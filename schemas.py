from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    productcontext: str
    stock: int = 0
    isactive: bool = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

# 🔥 FIXED: userid is now STRING, not int!
class UserBehaviorBase(BaseModel):
    userid: str  # ← CHANGED FROM int to str!
    productid: Optional[int] = None
    action: str
    searchquery: Optional[str] = None

class UserBehaviorCreate(UserBehaviorBase):
    pass

class Recommendation(BaseModel):
    product_id: int
    name: str
    price: float
    similarity_score: float
    match_percentage: float

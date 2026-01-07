from sqlalchemy.orm import Session
from models import Product, UserBehavior
from schemas import ProductCreate, UserBehaviorCreate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(
        Product.isactive == True, 
        Product.stock > 0
    ).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.isactive == True).first()

def create_user_behavior(db: Session, behavior: UserBehaviorCreate):
    db_behavior = UserBehavior(**behavior.dict())
    db.add(db_behavior)
    db.commit()
    db.refresh(db_behavior)
    return db_behavior

def get_user_behaviors(db: Session, user_id: int):  # ← user_id is STRING, not int!
    return db.query(UserBehavior).filter(UserBehavior.userid == user_id).all()


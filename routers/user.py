from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from crud import get_products, get_product, create_user_behavior, get_user_behaviors
from schemas import UserBehaviorCreate
from models import Product

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def store_home(request: Request, db: Session = Depends(get_db)):
    products = get_products(db)
    return templates.TemplateResponse("user/index.html", {
        "request": request, 
        "products": products
    })

@router.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(
    request: Request,  # ← THIS WAS MISSING!
    product_id: int,
    user_id: str = "demo_user_1",
    db: Session = Depends(get_db)
):
    """Product detail page - TRACKS VIEW BEHAVIOR"""
    
    # TRACK VIEW BEHAVIOR
    behavior = UserBehaviorCreate(
        userid=user_id,
        productid=product_id,
        action="view"
    )
    create_user_behavior(db, behavior)
    
    product = get_product(db, product_id)
    if not product:
        return HTMLResponse("Product not found", status_code=404)
    
    return templates.TemplateResponse("user/product_detail.html", {
        "request": request,  # ← THIS WAS MISSING!
        "product": product,
        "user_id": user_id
    })

@router.get("/search", response_class=HTMLResponse)
async def search_products(
    request: Request,  # ← THIS WAS MISSING!
    q: str = Query(""),
    user_id: str = "demo_user_1",
    db: Session = Depends(get_db)
):
    """Search products - TRACKS SEARCH BEHAVIOR"""
    
    # TRACK SEARCH BEHAVIOR
    if q.strip():
        behavior = UserBehaviorCreate(
            userid=user_id,
            productid=None,
            action="search",
            searchquery=q.strip()
        )
        create_user_behavior(db, behavior)
    
    products = get_products(db)
    if q.strip():
        products = [p for p in products if 
                   q.lower() in p.name.lower() or 
                   q.lower() in p.description.lower() if p.description]
    
    return templates.TemplateResponse("user/search.html", {
        "request": request,  # ← THIS WAS MISSING!
        "products": products,
        "query": q
    })

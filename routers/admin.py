from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from crud import create_product, get_products
from schemas import ProductCreate
from models import Product

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin dashboard - list all products"""
    products = get_products(db)
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, 
        "products": products
    })

@router.get("/add", response_class=HTMLResponse)
async def add_product_form(request: Request):
    """Form to add new product"""
    return templates.TemplateResponse("admin/add_product.html", {"request": request})

@router.post("/add")
async def create_new_product(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(""),
    productcontext: str = Form(...),  # 🔥 CRITICAL FIELD!
    stock: int = Form(0),
    isactive: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Handle product creation"""
    product_data = ProductCreate(
        name=name,
        price=price,
        description=description,
        productcontext=productcontext,
        stock=stock,
        isactive=isactive
    )
    product = create_product(db, product_data)
    return RedirectResponse(url="/admin/", status_code=303)

@router.get("/toggle/{product_id}")
async def toggle_product(product_id: int, db: Session = Depends(get_db)):
    """Toggle product active/inactive"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.isactive = not product.isactive
        db.commit()
    return RedirectResponse(url="/admin/", status_code=303)

# Add to END of routers/admin.py (before last line)
from datetime import datetime
from models import UserBehavior

@app.get("/admin/seed-demo")
async def seed_demo_data(db: Session = Depends(get_db)):
    """🚀 ONE-CLICK: Add demo user behaviors for ML recommendations!"""
    
    # Demo user history (matches your products)
    demo_behaviors = [
        {"userid": "demo_user_1", "productid": 1, "action": "view", "searchquery": "mobile phone", "timestamp": datetime.utcnow()},
        {"userid": "demo_user_1", "productid": 2, "action": "view", "searchquery": "samsung galaxy", "timestamp": datetime.utcnow()},
        {"userid": "demo_user_1", "productid": 5, "action": "view", "searchquery": "shoes fashion", "timestamp": datetime.utcnow()},
        {"userid": "demo_user_1", "productid": 9, "action": "click", "searchquery": "pressure cooker", "timestamp": datetime.utcnow()},
        {"userid": "demo_user_1", "productid": 13, "action": "add_to_cart", "searchquery": "skincare cream", "timestamp": datetime.utcnow()},
    ]
    
    added = 0
    for behavior_data in demo_behaviors:
        # Check if exists
        existing = db.query(UserBehavior).filter(
            UserBehavior.userid == behavior_data["userid"],
            UserBehavior.productid == behavior_data["productid"]
        ).first()
        
        if not existing:
            behavior = UserBehavior(**behavior_data)
            db.add(behavior)
            added += 1
    
    db.commit()
    return {
        "message": f"✅ Seeded {added} demo behaviors!",
        "total_behaviors": db.query(UserBehavior).count(),
        "demo_user_history": len(demo_behaviors)
    }

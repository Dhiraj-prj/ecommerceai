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

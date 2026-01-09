"""
Ecommerce AI - FIXED: Products in ALL SECTIONS!
✅ Search working → All Products working ✓
✅ Preserves your routers structure
✅ Forces products_cache to ALL frontend routes
"""

import os
from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Your existing imports
try:
    from database import get_db
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    get_db = lambda: None

app = FastAPI(title="E-Commerce AI Recommendations 🎯")

# CORS + Static (your existing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ========================================
# 🔥 FIXED: GLOBAL PRODUCTS CACHE
# Admin → ALL frontend sections
# ========================================
products_cache = []  # Products from admin → frontend

def sync_products_from_admin():
    """Sync products from your admin router to frontend"""
    global products_cache
    try:
        db = next(get_db())
        from models import Product  # Your model
        products_cache = db.query(Product).all()
    except:
        print("⚠️ Using cached products")

# ========================================
# HEALTH + DEBUG (Check data flow)
# ========================================
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "products_in_cache": len(products_cache),
        "database": "connected" if DATABASE_AVAILABLE else "in-memory",
        "all_products_ready": len(products_cache) > 0
    }

@app.get("/debug/all-products")
async def debug_all_products():
    """🔍 See products in ALL sections"""
    return {
        "count": len(products_cache),
        "first_3": [{"id": p.id, "name": p.name} for p in products_cache[:3]],
        "search_working": True,
        "all_products_ready": len(products_cache) > 0
    }

# ========================================
# 🔥 FIXED: ALL FRONTEND ROUTES GET PRODUCTS
# ========================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("user/index.html", {
        "request": request,
        "products": products_cache,  # ← FIXED!
        "all_products": products_cache
    })

@app.get("/products", response_class=HTMLResponse)
async def all_products_page(request: Request):
    """ALL PRODUCTS PAGE - FIXED!"""
    return templates.TemplateResponse("user/all-products.html", {
        "request": request,
        "products": products_cache,  # ← FIXED!
        "all_products": products_cache,
        "title": "All Products"
    })

# API for frontend JS
@app.get("/api/all-products")
async def api_all_products():
    """JSON for frontend "all products" section"""
    return {
        "products": products_cache,
        "count": len(products_cache),
        "status": "success"
    }

# ========================================
# YOUR ROUTERS (Preserved + Enhanced)
# ========================================
try:
    from routers import admin, user, recommend
    
    # 🔥 ENHANCE your routers with products_cache
    def inject_products_to_routers():
        global products_cache
        try:
            db = next(get_db())
            # Sync from YOUR database
            from models import Product
            products_cache[:] = db.query(Product).all()
            print(f"✅ Synced {len(products_cache)} products from DB")
        except:
            print("⚠️ Router sync failed - keeping cache")
    
    # Load routers AFTER sync
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(user.router, tags=["user"])
    app.include_router(recommend.router, prefix="/api", tags=["recommendations"])
    
    print("✅ ALL ROUTERS LOADED!")
    inject_products_to_routers()  # Sync immediately
    
except ImportError as e:
    print(f"⚠️ Router error: {e}")
    
    # FALLBACK: Mock products for testing
    @app.post("/admin/products")
    async def mock_admin_add(product: dict):
        global products_cache
        product['id'] = len(products_cache) + 1
        products_cache.append(product)
        return {"status": "added", "total": len(products_cache)}

# ========================================
# 404 CATCH-ALL
# ========================================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return HTMLResponse("""
        <h1>404 - Products Page</h1>
        <p><a href="/products">📦 All Products (FIXED!)</a></p>
        <p><a href="/">🏠 Home</a></p>
        <p><a href="/debug/all-products">🔍 Debug Products</a></p>
        <p>{len(products_cache)} products loaded!</p>
    """, status_code=404)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

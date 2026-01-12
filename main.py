import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI(title="E-Commerce AI Recommendations 🎯")

# app.mount("/static", StaticFiles(directory="static"), name="static")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    print("Static directory not found - skipping mount")

templates = Jinja2Templates(directory="templates")

# 🔥 CRITICAL: Include ALL routers
try:
    from routers import admin, user, recommend
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(user.router, tags=["user"])
    app.include_router(recommend.router, prefix="/api", tags=["recommendations"])
    print("✅ ALL ROUTERS LOADED!")
except ImportError as e:
    print(f"❌ Router error: {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "All systems ready!"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("user/index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

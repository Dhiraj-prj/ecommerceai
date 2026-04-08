EcommerceAI - AI-Powered E-Commerce Platform
[
[
[

EcommerceAI is a full-stack e-commerce platform with content-based AI recommendations using TF-IDF + Cosine Similarity. Built for production with FastAPI, SQLAlchemy, and Jinja2 templates.

🚀 Features
AI Recommendations: TF-IDF + Cosine Similarity for personalized product suggestions

Product Management: CRUD operations with admin panel

Search: Real-time product search across name + description

Responsive UI: Clean Jinja2 templates with Bootstrap

Production Ready: Railway deployment, Postgres/SQLite compatible

API Endpoints: /api/recommendations, /api/test, health checks

🛠 Tech Stack
Frontend	Backend	Database	Deployment
Jinja2 + Bootstrap	FastAPI + Routers	SQLAlchemy (SQLite/Postgres)	Railway + Uvicorn
Static Files	scikit-learn (ML)	Auto table creation	GitHub Actions
📁 Project Structure
text
ecommerceai/
├── main.py                 # FastAPI app entrypoint
├── database.py            # DB session management
├── crud.py               # Product CRUD operations
├── models.py             # SQLAlchemy models
├── routers/
│   ├── __init__.py
│   ├── admin.py          # Admin panel
│   └── user.py           # User pages (/products, /search)
├── templates/
│   └── user/             # HTML templates
└── static/               # CSS, JS, images
    └── app.db            # SQLite database
🚀 Quick Start (Local)
Clone & Install

bash
git clone https://github.com/yourusername/ecommerceai.git
cd ecommerceai
pip install -r requirements.txt
Run Server

bash
python -m uvicorn main:app --reload
Visit

text
http://localhost:8000          # Home
http://localhost:8000/products # All Products
http://localhost:8000/search   # Search
http://localhost:8000/admin    # Admin Panel
http://localhost:8000/docs     # API Docs
🌐 Production Deployment (Railway)
Push to GitHub

bash
git add .
git commit -m "Deploy EcommerceAI"
git push origin main
Railway Setup

text
✅ Auto-deploys on every push! Tables auto-created.

🧠 AI Recommendations
How it works:

text
1. TF-IDF Vectorization → Product descriptions
2. Cosine Similarity → User behavior vs Products  
3. Top-N recommendations → Personalized suggestions
API Endpoint:

text
GET /api/recommendations?user_id=1&limit=5
📊 Database Schema
sql
products: id, name, price, description, image_url
user_behaviors: user_id, product_id, interaction_type, timestamp
🔧 Environment Variables
text
DATABASE_URL=sqlite:///app.db    # Local
DATABASE_URL=postgresql://...    # Railway Postgres
SECRET_KEY=your-secret-key
🐛 Troubleshooting
Issue	Solution
no such table	Tables auto-created on startup
Windows multiprocessing	Use python -m uvicorn main:app
404 on /products	Router fixed in user.py
ML import error	pip install scikit-learn
📈 API Documentation
Auto-generated at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Key Endpoints:

text
GET  /                    # Home page
GET  /products           # All products
GET  /search?q=phone     # Search products
GET  /product/{id}       # Product detail
GET  /admin              # Admin panel
POST /api/recommendations # AI recommendations
🤝 Contributing
Fork the repo

Create feature branch (git checkout -b feature/product-filter)

Commit changes (git commit -m 'Add product filter')

Push (git push origin feature/product-filter)

Open Pull Request

📄 License
MIT License - Free to use, modify, deploy anywhere!

🙌 Acknowledgments
Built with ❤️ for Nepali developers. Perfect for e-commerce startups, student projects, and production apps.

⭐ Star this repo if it helps you!
Made in Nepal 🇳🇵 


from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    productcontext = Column(Text, nullable=False)  # CRITICAL for AI!
    stock = Column(Integer, default=0)
    isactive = Column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

class UserBehavior(Base):
    __tablename__ = "user_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"), nullable=False)
    productid = Column(Integer, ForeignKey("products.id"), nullable=True)
    action = Column(String(50), nullable=False)  # 'view', 'click', 'search'
    searchquery = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

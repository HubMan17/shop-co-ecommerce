from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    discount_percent = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    sizes = Column(JSON, default=list)  # ["S", "M", "L", "XL"]
    colors = Column(JSON, default=list)  # [{"name": "green", "hex": "#00FF00"}]
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    stock = Column(Integer, default=0)
    is_new_arrival = Column(Integer, default=0)  # Boolean as int for SQLite
    is_top_selling = Column(Integer, default=0)
    style = Column(String(100), nullable=True)  # casual, formal, party, gym
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String(500), nullable=False)
    is_primary = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")

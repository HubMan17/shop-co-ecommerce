from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="pending")  # pending, processing, shipped, delivered, cancelled
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    delivery_fee = Column(Float, default=0)
    total = Column(Float, nullable=False)
    promo_code = Column(String(50), nullable=True)
    shipping_address = Column(JSON, nullable=True)
    billing_address = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_image = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    size = Column(String(20), nullable=True)
    color = Column(String(50), nullable=True)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

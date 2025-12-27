from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    size: Optional[str] = None
    color: Optional[str] = None


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None
    subtotal: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    items: List[CartItemResponse] = []
    items_count: int
    subtotal: float
    discount: float = 0
    delivery_fee: float = 0
    total: float

    class Config:
        from_attributes = True

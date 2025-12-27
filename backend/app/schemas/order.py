from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AddressInfo(BaseModel):
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str = "US"


class OrderCreate(BaseModel):
    shipping_address: AddressInfo
    billing_address: Optional[AddressInfo] = None
    promo_code: Optional[str] = None
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    price: float
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: str
    subtotal: float
    discount: float
    delivery_fee: float
    total: float
    promo_code: Optional[str] = None
    shipping_address: Optional[dict] = None
    items: List[OrderItemResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

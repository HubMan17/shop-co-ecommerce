from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ColorOption(BaseModel):
    name: str
    hex: str


class ProductImageResponse(BaseModel):
    id: int
    url: str
    is_primary: bool

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    discount_percent: Optional[int] = None
    sizes: List[str] = []
    colors: List[ColorOption] = []
    rating: float = 0.0
    reviews_count: int = 0
    stock: int = 0
    is_new_arrival: bool = False
    is_top_selling: bool = False
    style: Optional[str] = None
    images: List[ProductImageResponse] = []
    category: Optional[CategoryResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    per_page: int
    pages: int

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List

from ..database import get_db
from ..models.product import Product, Category, ProductImage
from ..schemas.product import ProductResponse, ProductListResponse, CategoryResponse

router = APIRouter(prefix="/products", tags=["Products"])


def product_to_response(product: Product) -> dict:
    images = [{"id": img.id, "url": img.url, "is_primary": bool(img.is_primary)} for img in product.images]
    category = None
    if product.category:
        category = {
            "id": product.category.id,
            "name": product.category.name,
            "slug": product.category.slug,
            "description": product.category.description,
            "image_url": product.category.image_url,
        }

    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "price": product.price,
        "discount_price": product.discount_price,
        "discount_percent": product.discount_percent,
        "sizes": product.sizes or [],
        "colors": product.colors or [],
        "rating": product.rating,
        "reviews_count": product.reviews_count,
        "stock": product.stock,
        "is_new_arrival": bool(product.is_new_arrival),
        "is_top_selling": bool(product.is_top_selling),
        "style": product.style,
        "images": images,
        "category": category,
        "created_at": product.created_at,
    }


@router.get("", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    category: Optional[str] = None,
    style: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sizes: Optional[str] = None,
    colors: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "newest",
    db: AsyncSession = Depends(get_db)
):
    query = select(Product).options(selectinload(Product.images), selectinload(Product.category))
    count_query = select(func.count(Product.id))

    # Filters
    if category:
        cat_result = await db.execute(select(Category).where(Category.slug == category))
        cat = cat_result.scalar_one_or_none()
        if cat:
            query = query.where(Product.category_id == cat.id)
            count_query = count_query.where(Product.category_id == cat.id)

    if style:
        query = query.where(Product.style == style)
        count_query = count_query.where(Product.style == style)

    if min_price is not None:
        effective_price = func.coalesce(Product.discount_price, Product.price)
        query = query.where(effective_price >= min_price)
        count_query = count_query.where(effective_price >= min_price)

    if max_price is not None:
        effective_price = func.coalesce(Product.discount_price, Product.price)
        query = query.where(effective_price <= max_price)
        count_query = count_query.where(effective_price <= max_price)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
        count_query = count_query.where(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    # Sorting
    if sort == "newest":
        query = query.order_by(Product.created_at.desc())
    elif sort == "price_low":
        query = query.order_by(func.coalesce(Product.discount_price, Product.price).asc())
    elif sort == "price_high":
        query = query.order_by(func.coalesce(Product.discount_price, Product.price).desc())
    elif sort == "popular":
        query = query.order_by(Product.reviews_count.desc())
    elif sort == "rating":
        query = query.order_by(Product.rating.desc())

    # Count total
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    products = result.scalars().all()

    return ProductListResponse(
        items=[product_to_response(p) for p in products],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page
    )


@router.get("/new-arrivals", response_model=List[ProductResponse])
async def get_new_arrivals(
    limit: int = Query(4, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.category))
        .where(Product.is_new_arrival == 1)
        .order_by(Product.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    products = result.scalars().all()
    return [product_to_response(p) for p in products]


@router.get("/top-selling", response_model=List[ProductResponse])
async def get_top_selling(
    limit: int = Query(4, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.category))
        .where(Product.is_top_selling == 1)
        .order_by(Product.reviews_count.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    products = result.scalars().all()
    return [product_to_response(p) for p in products]


@router.get("/{slug}", response_model=ProductResponse)
async def get_product(slug: str, db: AsyncSession = Depends(get_db)):
    query = (
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.category))
        .where(Product.slug == slug)
    )
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_to_response(product)

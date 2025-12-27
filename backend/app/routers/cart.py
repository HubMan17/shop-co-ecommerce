from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
import uuid

from ..database import get_db
from ..models.cart import Cart, CartItem
from ..models.product import Product
from ..models.user import User
from ..schemas.cart import CartResponse, CartItemCreate, CartItemUpdate
from ..utils.security import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


async def get_or_create_cart(
    db: AsyncSession,
    user: Optional[User] = None,
    session_id: Optional[str] = None
) -> Cart:
    if user:
        result = await db.execute(
            select(Cart)
            .options(selectinload(Cart.items))
            .where(Cart.user_id == user.id)
        )
        cart = result.scalar_one_or_none()
        if not cart:
            cart = Cart(user_id=user.id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
    else:
        if session_id:
            result = await db.execute(
                select(Cart)
                .options(selectinload(Cart.items))
                .where(Cart.session_id == session_id)
            )
            cart = result.scalar_one_or_none()
            if cart:
                return cart
        cart = Cart(session_id=session_id or str(uuid.uuid4()))
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
    return cart


def cart_to_response(cart: Cart, items_with_products: list) -> dict:
    cart_items = []
    subtotal = 0

    for item, product in items_with_products:
        price = product.discount_price or product.price
        item_subtotal = price * item.quantity
        subtotal += item_subtotal

        primary_image = None
        if product.images:
            primary = next((img for img in product.images if img.is_primary), None)
            primary_image = primary.url if primary else product.images[0].url if product.images else None

        cart_items.append({
            "id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "product_image": primary_image,
            "price": product.price,
            "discount_price": product.discount_price,
            "quantity": item.quantity,
            "size": item.size,
            "color": item.color,
            "subtotal": item_subtotal,
        })

    delivery_fee = 15.0 if subtotal > 0 and subtotal < 200 else 0
    total = subtotal + delivery_fee

    return {
        "id": cart.id,
        "items": cart_items,
        "items_count": len(cart_items),
        "subtotal": subtotal,
        "discount": 0,
        "delivery_fee": delivery_fee,
        "total": total,
    }


@router.get("", response_model=CartResponse)
async def get_cart(
    request: Request,
    user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session_id = request.cookies.get("cart_session")
    cart = await get_or_create_cart(db, user, session_id)

    # Load items with products
    items_result = await db.execute(
        select(CartItem, Product)
        .join(Product)
        .options(selectinload(Product.images))
        .where(CartItem.cart_id == cart.id)
    )
    items_with_products = items_result.all()

    return cart_to_response(cart, items_with_products)


@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    item_data: CartItemCreate,
    request: Request,
    user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check product exists
    product_result = await db.execute(select(Product).where(Product.id == item_data.product_id))
    product = product_result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session_id = request.cookies.get("cart_session")
    cart = await get_or_create_cart(db, user, session_id)

    # Check if item already in cart
    existing_result = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item_data.product_id,
            CartItem.size == item_data.size,
            CartItem.color == item_data.color
        )
    )
    existing_item = existing_result.scalar_one_or_none()

    if existing_item:
        existing_item.quantity += item_data.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            size=item_data.size,
            color=item_data.color
        )
        db.add(cart_item)

    await db.commit()

    # Reload cart
    items_result = await db.execute(
        select(CartItem, Product)
        .join(Product)
        .options(selectinload(Product.images))
        .where(CartItem.cart_id == cart.id)
    )
    items_with_products = items_result.all()

    return cart_to_response(cart, items_with_products)


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    request: Request,
    user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session_id = request.cookies.get("cart_session")
    cart = await get_or_create_cart(db, user, session_id)

    result = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    )
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if item_data.quantity <= 0:
        await db.delete(cart_item)
    else:
        cart_item.quantity = item_data.quantity

    await db.commit()

    # Reload cart
    items_result = await db.execute(
        select(CartItem, Product)
        .join(Product)
        .options(selectinload(Product.images))
        .where(CartItem.cart_id == cart.id)
    )
    items_with_products = items_result.all()

    return cart_to_response(cart, items_with_products)


@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_cart_item(
    item_id: int,
    request: Request,
    user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session_id = request.cookies.get("cart_session")
    cart = await get_or_create_cart(db, user, session_id)

    result = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart.id)
    )
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await db.delete(cart_item)
    await db.commit()

    # Reload cart
    items_result = await db.execute(
        select(CartItem, Product)
        .join(Product)
        .options(selectinload(Product.images))
        .where(CartItem.cart_id == cart.id)
    )
    items_with_products = items_result.all()

    return cart_to_response(cart, items_with_products)

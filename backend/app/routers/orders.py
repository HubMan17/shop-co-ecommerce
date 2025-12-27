from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from ..database import get_db
from ..models.cart import Cart, CartItem
from ..models.product import Product
from ..models.order import Order, OrderItem
from ..models.user import User
from ..schemas.order import OrderCreate, OrderResponse
from ..utils.security import get_current_user, get_current_user_required

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    request: Request,
    user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    # Get user's cart
    cart_result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items))
        .where(Cart.user_id == user.id)
    )
    cart = cart_result.scalar_one_or_none()

    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Load cart items with products
    items_result = await db.execute(
        select(CartItem, Product)
        .join(Product)
        .options(selectinload(Product.images))
        .where(CartItem.cart_id == cart.id)
    )
    items_with_products = items_result.all()

    # Calculate totals
    subtotal = 0
    order_items = []

    for cart_item, product in items_with_products:
        price = product.discount_price or product.price
        subtotal += price * cart_item.quantity

        primary_image = None
        if product.images:
            primary = next((img for img in product.images if img.is_primary), None)
            primary_image = primary.url if primary else product.images[0].url if product.images else None

        order_items.append(OrderItem(
            product_id=product.id,
            product_name=product.name,
            product_image=primary_image,
            price=price,
            quantity=cart_item.quantity,
            size=cart_item.size,
            color=cart_item.color
        ))

    delivery_fee = 15.0 if subtotal < 200 else 0
    discount = 0

    # Apply promo code (simple example)
    if order_data.promo_code and order_data.promo_code.upper() == "SAVE20":
        discount = subtotal * 0.20

    total = subtotal - discount + delivery_fee

    # Create order
    order = Order(
        user_id=user.id,
        subtotal=subtotal,
        discount=discount,
        delivery_fee=delivery_fee,
        total=total,
        promo_code=order_data.promo_code,
        shipping_address=order_data.shipping_address.model_dump(),
        billing_address=order_data.billing_address.model_dump() if order_data.billing_address else None,
        notes=order_data.notes,
        status="pending"
    )
    order.items = order_items
    db.add(order)

    # Clear cart
    for cart_item, _ in items_with_products:
        await db.delete(cart_item)

    await db.commit()
    await db.refresh(order)

    return order


@router.get("", response_model=List[OrderResponse])
async def get_orders(
    user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id, Order.user_id == user.id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

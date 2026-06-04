from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product_variant import ProductVariant
from app.models.stock import StockHistory


ALLOWED_ORDER_STATUSES = ["pending", "paid", "cancelled", "refunded"]


def generate_order_number():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"ORD-{timestamp}"


def create_order(db: Session, order_data):
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must have at least one item"
        )

    if order_data.discount < 0:
        raise HTTPException(
            status_code=400,
            detail="Discount cannot be negative"
        )

    customer = db.query(Customer).filter(
        Customer.id == order_data.customer_id,
        Customer.is_active.is_(True)
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    seen_variant_ids = set()
    checked_items = []
    total_amount = 0

    for item in order_data.items:
        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than zero"
            )

        if item.variant_id in seen_variant_ids:
            raise HTTPException(
                status_code=400,
                detail="Duplicate variant is not allowed in same order"
            )

        seen_variant_ids.add(item.variant_id)

        variant = db.query(ProductVariant).filter(
            ProductVariant.id == item.variant_id,
            ProductVariant.is_active.is_(True)
        ).first()

        if not variant:
            raise HTTPException(
                status_code=404,
                detail=f"Variant {item.variant_id} not found"
            )

        if variant.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for variant {item.variant_id}"
            )

        item_total = variant.sell_price * item.quantity
        total_amount += item_total

        checked_items.append({
            "variant": variant,
            "quantity": item.quantity,
            "unit_price": variant.sell_price,
            "total_price": item_total
        })

    if order_data.discount > total_amount:
        raise HTTPException(
            status_code=400,
            detail="Discount cannot be greater than total amount"
        )

    final_amount = total_amount - order_data.discount

    new_order = Order(
        customer_id=order_data.customer_id,
        order_number=generate_order_number(),
        total_amount=total_amount,
        discount=order_data.discount,
        final_amount=final_amount,
        status="pending",
        created_by=order_data.created_by
    )

    db.add(new_order)
    db.flush()

    for item in checked_items:
        variant = item["variant"]
        previous_stock = variant.stock_quantity
        new_stock = previous_stock - item["quantity"]

        variant.stock_quantity = new_stock

        order_item = OrderItem(
            order_id=new_order.id,
            variant_id=variant.id,
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            total_price=item["total_price"]
        )

        stock_history = StockHistory(
            variant_id=variant.id,
            change_type="sale",
            quantity=item["quantity"],
            previous_stock=previous_stock,
            new_stock=new_stock,
            note=f"Stock reduced for order {new_order.order_number}",
            created_by=order_data.created_by
        )

        db.add(order_item)
        db.add(stock_history)

    db.commit()
    db.refresh(new_order)

    return new_order


def update_order_status(db: Session, order_id: int, new_status: str):
    if new_status not in ALLOWED_ORDER_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status in ["cancelled", "refunded"]:
        raise HTTPException(
            status_code=400,
            detail="Cancelled or refunded order cannot be updated"
        )

    if new_status in ["cancelled", "refunded"] and order.status not in ["cancelled", "refunded"]:
        for item in order.items:
            variant = db.query(ProductVariant).filter(
                ProductVariant.id == item.variant_id
            ).first()

            previous_stock = variant.stock_quantity
            new_stock = previous_stock + item.quantity

            variant.stock_quantity = new_stock

            stock_history = StockHistory(
                variant_id=variant.id,
                change_type="return",
                quantity=item.quantity,
                previous_stock=previous_stock,
                new_stock=new_stock,
                note=f"Stock returned for order {order.order_number}",
                created_by=order.created_by
            )

            db.add(stock_history)

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order

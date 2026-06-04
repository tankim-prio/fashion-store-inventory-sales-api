from datetime import date

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.product import Product
from app.models.product_variant import ProductVariant


INVALID_ORDER_STATUSES = ["cancelled", "refunded"]


def _valid_orders_query(db: Session):
    return db.query(Order).filter(
        ~Order.status.in_(INVALID_ORDER_STATUSES)
    )


def _calculate_paid_amount(db: Session, order_ids: list[int]):
    if not order_ids:
        return 0

    total_paid = db.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).filter(
        Payment.order_id.in_(order_ids),
        Payment.status == "paid"
    ).scalar()

    return float(total_paid or 0)


def get_daily_sales_report(db: Session, report_date: date):
    orders = _valid_orders_query(db).filter(
        func.date(Order.created_at) == report_date
    ).all()

    order_ids = [order.id for order in orders]

    total_sales_amount = sum(order.total_amount for order in orders)
    total_discount = sum(order.discount for order in orders)
    total_revenue = sum(order.final_amount for order in orders)
    total_paid = _calculate_paid_amount(db, order_ids)
    total_due = total_revenue - total_paid

    return {
        "report_date": report_date,
        "total_orders": len(orders),
        "total_sales_amount": total_sales_amount,
        "total_discount": total_discount,
        "total_revenue": total_revenue,
        "total_paid": total_paid,
        "total_due": total_due
    }


def get_monthly_sales_report(db: Session, year: int, month: int):
    orders = _valid_orders_query(db).filter(
        extract("year", Order.created_at) == year,
        extract("month", Order.created_at) == month
    ).all()

    order_ids = [order.id for order in orders]

    total_sales_amount = sum(order.total_amount for order in orders)
    total_discount = sum(order.discount for order in orders)
    total_revenue = sum(order.final_amount for order in orders)
    total_paid = _calculate_paid_amount(db, order_ids)
    total_due = total_revenue - total_paid

    return {
        "year": year,
        "month": month,
        "total_orders": len(orders),
        "total_sales_amount": total_sales_amount,
        "total_discount": total_discount,
        "total_revenue": total_revenue,
        "total_paid": total_paid,
        "total_due": total_due
    }


def get_top_products_report(db: Session, limit: int = 5):
    results = db.query(
        OrderItem.variant_id,
        Product.name.label("product_name"),
        ProductVariant.size,
        ProductVariant.color,
        ProductVariant.sku,
        func.coalesce(func.sum(OrderItem.quantity), 0).label("total_quantity_sold"),
        func.coalesce(func.sum(OrderItem.total_price), 0).label("total_sales")
    ).join(
        Order, Order.id == OrderItem.order_id
    ).join(
        ProductVariant, ProductVariant.id == OrderItem.variant_id
    ).join(
        Product, Product.id == ProductVariant.product_id
    ).filter(
        ~Order.status.in_(INVALID_ORDER_STATUSES)
    ).group_by(
        OrderItem.variant_id,
        Product.name,
        ProductVariant.size,
        ProductVariant.color,
        ProductVariant.sku
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(limit).all()

    return [
        {
            "variant_id": row.variant_id,
            "product_name": row.product_name,
            "size": row.size,
            "color": row.color,
            "sku": row.sku,
            "total_quantity_sold": int(row.total_quantity_sold or 0),
            "total_sales": float(row.total_sales or 0)
        }
        for row in results
    ]


def get_profit_report(db: Session):
    result = db.query(
        func.coalesce(func.sum(OrderItem.total_price), 0).label("total_sales"),
        func.coalesce(
            func.sum(OrderItem.quantity * ProductVariant.buy_price),
            0
        ).label("total_buy_cost")
    ).join(
        Order, Order.id == OrderItem.order_id
    ).join(
        ProductVariant, ProductVariant.id == OrderItem.variant_id
    ).filter(
        ~Order.status.in_(INVALID_ORDER_STATUSES)
    ).first()

    total_sales = float(result.total_sales or 0)
    total_buy_cost = float(result.total_buy_cost or 0)
    total_profit = total_sales - total_buy_cost

    return {
        "total_sales": total_sales,
        "total_buy_cost": total_buy_cost,
        "total_profit": total_profit
    }


def get_low_stock_report(db: Session, threshold: int = 5):
    variants = db.query(
        ProductVariant.id.label("variant_id"),
        ProductVariant.product_id,
        Product.name.label("product_name"),
        ProductVariant.size,
        ProductVariant.color,
        ProductVariant.sku,
        ProductVariant.stock_quantity
    ).join(
        Product, Product.id == ProductVariant.product_id
    ).filter(
        ProductVariant.is_active.is_(True),
        ProductVariant.stock_quantity <= threshold
    ).all()

    return [
        {
            "variant_id": row.variant_id,
            "product_id": row.product_id,
            "product_name": row.product_name,
            "size": row.size,
            "color": row.color,
            "sku": row.sku,
            "stock_quantity": row.stock_quantity
        }
        for row in variants
    ]

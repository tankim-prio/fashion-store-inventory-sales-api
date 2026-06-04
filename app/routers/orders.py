from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import create_order, update_order_status

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order_data=order)


@router.get("/", response_model=list[OrderResponse])
def get_orders(
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Order)

    if customer_id:
        query = query.filter(Order.customer_id == customer_id)

    if status:
        query = query.filter(Order.status == status)

    return query.order_by(Order.id.desc()).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    return update_order_status(
        db=db,
        order_id=order_id,
        new_status=status_data.status
    )

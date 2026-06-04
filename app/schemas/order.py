from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    variant_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]
    discount: float = 0
    created_by: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: str


class OrderItemResponse(BaseModel):
    id: int
    variant_id: int
    quantity: int
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    order_number: str
    total_amount: float
    discount: float
    final_amount: float
    status: str
    created_by: Optional[str] = None
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

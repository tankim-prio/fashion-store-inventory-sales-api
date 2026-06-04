from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductVariantCreate(BaseModel):
    product_id: int
    size: str
    color: str
    buy_price: float
    sell_price: float
    stock_quantity: int = 0
    sku: str


class ProductVariantUpdate(BaseModel):
    product_id: Optional[int] = None
    size: Optional[str] = None
    color: Optional[str] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    sku: Optional[str] = None
    is_active: Optional[bool] = None


class ProductVariantResponse(BaseModel):
    id: int
    product_id: int
    size: str
    color: str
    buy_price: float
    sell_price: float
    stock_quantity: int
    sku: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

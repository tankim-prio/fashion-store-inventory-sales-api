from datetime import date
from typing import Optional

from pydantic import BaseModel


class SalesReportResponse(BaseModel):
    report_date: Optional[date] = None
    year: Optional[int] = None
    month: Optional[int] = None
    total_orders: int
    total_sales_amount: float
    total_discount: float
    total_revenue: float
    total_paid: float
    total_due: float


class TopProductResponse(BaseModel):
    variant_id: int
    product_name: str
    size: str
    color: str
    sku: str
    total_quantity_sold: int
    total_sales: float


class ProfitReportResponse(BaseModel):
    total_sales: float
    total_buy_cost: float
    total_profit: float


class LowStockReportResponse(BaseModel):
    variant_id: int
    product_id: int
    product_name: str
    size: str
    color: str
    sku: str
    stock_quantity: int

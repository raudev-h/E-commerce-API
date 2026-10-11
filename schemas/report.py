from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
import enum


class ReportGranularity(str, enum.Enum):
    day = "day"
    month = "month"


class SalesReportRow(BaseModel):
    period: datetime
    orders_count: int
    total_revenue: Decimal
    average_ticket: Decimal


class SalesReportResponse(BaseModel):
    start_date: date
    end_date: date
    granularity: ReportGranularity
    total_orders: int
    grand_total: Decimal
    rows: list[SalesReportRow]


class TopProductRow(BaseModel):
    product_id: UUID
    product_name: str
    units_sold: int
    revenue: Decimal


class TopProductsReportResponse(BaseModel):
    start_date: date
    end_date: date
    rows: list[TopProductRow]


class LowStockRow(BaseModel):
    product_id: UUID
    product_name: str
    category_name: str | None
    stock: int


class LowStockReportResponse(BaseModel):
    threshold: int
    total_products: int
    rows: list[LowStockRow]

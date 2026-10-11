from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import RowMapping, func, select
from models import Order, OrderItem, Product, Category, Status
from collections.abc import Sequence
from datetime import datetime


async def get_sales_by_period(
    db: AsyncSession,
    range_start: datetime,
    range_end: datetime,
    granularity: str,
    excluded_statuses: Sequence[Status],
) -> Sequence[RowMapping]:
    period = func.date_trunc(granularity, Order.created_at).label("period")

    result = await db.execute(
        select(
            period,
            func.count(Order.id).label("orders_count"),
            func.sum(Order.total).label("total_revenue"),
            func.avg(Order.total).label("average_ticket"),
        )
        .where(
            Order.created_at >= range_start,
            Order.created_at < range_end,
            Order.status.not_in(excluded_statuses),
        )
        .group_by(period)
        .order_by(period)
    )
    return result.mappings().all()


async def get_top_products(
    db: AsyncSession,
    range_start: datetime,
    range_end: datetime,
    excluded_statuses: Sequence[Status],
    limit: int,
) -> Sequence[RowMapping]:
    units_sold = func.sum(OrderItem.quantity).label("units_sold")

    result = await db.execute(
        select(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            units_sold,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
        )
        .join(Order, Order.id == OrderItem.order_id)
        .join(Product, Product.id == OrderItem.product_id)
        .where(
            Order.created_at >= range_start,
            Order.created_at < range_end,
            Order.status.not_in(excluded_statuses),
        )
        .group_by(Product.id, Product.name)
        .order_by(units_sold.desc(), Product.name.asc())
        .limit(limit)
    )
    return result.mappings().all()


async def get_low_stock_products(
    db: AsyncSession, threshold: int
) -> Sequence[RowMapping]:
    result = await db.execute(
        select(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Category.name.label("category_name"),
            Product.stock.label("stock"),
        )
        .outerjoin(Category, Category.id == Product.category_id)
        .where(Product.stock <= threshold)
        .order_by(Product.stock.asc(), Product.name.asc())
    )
    return result.mappings().all()

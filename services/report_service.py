from sqlalchemy.ext.asyncio import AsyncSession
from core import BadRequestException
from models import Status
from schemas import (
    ReportGranularity,
    SalesReportRow,
    SalesReportResponse,
    TopProductRow,
    TopProductsReportResponse,
    LowStockRow,
    LowStockReportResponse,
)
from repositories import report_repository
from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP

EXCLUDED_ORDER_STATUSES: tuple[Status, ...] = (Status.CANCELLED,)
MAX_REPORT_RANGE_DAYS: int = 366
DEFAULT_LOW_STOCK_THRESHOLD: int = 5
DEFAULT_TOP_PRODUCTS_LIMIT: int = 10
MAX_TOP_PRODUCTS_LIMIT: int = 50
MONEY_PRECISION: Decimal = Decimal("0.01")


async def get_sales_report(
    db: AsyncSession,
    start_date: date,
    end_date: date,
    granularity: ReportGranularity,
) -> SalesReportResponse:
    range_start, range_end = _to_datetime_range(start_date, end_date)

    sales = await report_repository.get_sales_by_period(
        db, range_start, range_end, granularity.value, EXCLUDED_ORDER_STATUSES
    )

    return SalesReportResponse(
        start_date=start_date,
        end_date=end_date,
        granularity=granularity,
        total_orders=sum(row["orders_count"] for row in sales),
        grand_total=_to_money(sum(row["total_revenue"] for row in sales)),
        rows=[
            SalesReportRow(
                period=row["period"],
                orders_count=row["orders_count"],
                total_revenue=_to_money(row["total_revenue"]),
                average_ticket=_to_money(row["average_ticket"]),
            )
            for row in sales
        ],
    )


async def get_top_products_report(
    db: AsyncSession, start_date: date, end_date: date, limit: int
) -> TopProductsReportResponse:
    range_start, range_end = _to_datetime_range(start_date, end_date)

    products = await report_repository.get_top_products(
        db, range_start, range_end, EXCLUDED_ORDER_STATUSES, limit
    )

    return TopProductsReportResponse(
        start_date=start_date,
        end_date=end_date,
        rows=[
            TopProductRow(
                product_id=row["product_id"],
                product_name=row["product_name"],
                units_sold=row["units_sold"],
                revenue=_to_money(row["revenue"]),
            )
            for row in products
        ],
    )


async def get_low_stock_report(
    db: AsyncSession, threshold: int
) -> LowStockReportResponse:
    products = await report_repository.get_low_stock_products(db, threshold)

    return LowStockReportResponse(
        threshold=threshold,
        total_products=len(products),
        rows=[LowStockRow(**row) for row in products],
    )


def _to_datetime_range(start_date: date, end_date: date) -> tuple[datetime, datetime]:
    if start_date > end_date:
        raise BadRequestException("start_date must be before or equal to end_date")

    if (end_date - start_date).days > MAX_REPORT_RANGE_DAYS:
        raise BadRequestException(
            f"date range cannot exceed {MAX_REPORT_RANGE_DAYS} days"
        )

    # created_at es naive en los modelos; el fin es exclusivo para incluir todo el último día
    range_start = datetime.combine(start_date, time.min)
    range_end = datetime.combine(end_date + timedelta(days=1), time.min)

    return range_start, range_end


def _to_money(amount: float | Decimal) -> Decimal:
    return Decimal(str(amount)).quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)

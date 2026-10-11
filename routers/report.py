from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core import security
from schemas import (
    ReportGranularity,
    SalesReportResponse,
    TopProductsReportResponse,
    LowStockReportResponse,
)
from services import report_service
from datetime import date
from typing import Annotated

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(security.get_current_admin)],
)


@router.get("/sales", response_model=SalesReportResponse)
async def get_sales_report(
    start_date: date,
    end_date: date,
    granularity: ReportGranularity = ReportGranularity.day,
    db: AsyncSession = Depends(get_db),
) -> SalesReportResponse:
    return await report_service.get_sales_report(db, start_date, end_date, granularity)


@router.get("/top-products", response_model=TopProductsReportResponse)
async def get_top_products_report(
    start_date: date,
    end_date: date,
    limit: Annotated[
        int, Query(ge=1, le=report_service.MAX_TOP_PRODUCTS_LIMIT)
    ] = report_service.DEFAULT_TOP_PRODUCTS_LIMIT,
    db: AsyncSession = Depends(get_db),
) -> TopProductsReportResponse:
    return await report_service.get_top_products_report(db, start_date, end_date, limit)


@router.get("/low-stock", response_model=LowStockReportResponse)
async def get_low_stock_report(
    threshold: Annotated[int, Query(ge=0)] = report_service.DEFAULT_LOW_STOCK_THRESHOLD,
    db: AsyncSession = Depends(get_db),
) -> LowStockReportResponse:
    return await report_service.get_low_stock_report(db, threshold)

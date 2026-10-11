import pytest
import pytest_asyncio
from decimal import Decimal
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from models import Order, OrderItem, Product, Status


async def seed_product(
    db_session: AsyncSession, category_id: str, name: str, price: float, stock: int
) -> Product:
    product = Product(name=name, price=price, stock=stock, category_id=category_id)
    db_session.add(product)
    await db_session.flush()
    return product


async def seed_order(
    db_session: AsyncSession,
    user_id: str,
    created_at: datetime,
    status: Status,
    items: list[tuple[Product, int]],
) -> Order:
    order = Order(
        user_id=user_id,
        status=status,
        created_at=created_at,
        total=sum(product.price * quantity for product, quantity in items),
    )
    db_session.add(order)
    await db_session.flush()

    for product, quantity in items:
        db_session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
            )
        )
    await db_session.flush()
    return order


@pytest_asyncio.fixture
async def seeded_sales(db_session: AsyncSession, created_user: dict, created_category: dict):
    mouse = await seed_product(db_session, created_category["id"], "Wireless Mouse", 20, 50)
    keyboard = await seed_product(db_session, created_category["id"], "Keyboard", 45.5, 50)

    await seed_order(
        db_session, created_user["id"], datetime(2026, 1, 5, 10, 0), Status.PENDING, [(mouse, 3)]
    )
    await seed_order(
        db_session,
        created_user["id"],
        datetime(2026, 1, 31, 23, 59),
        Status.DELIVERED,
        [(mouse, 2), (keyboard, 2)],
    )
    await seed_order(
        db_session, created_user["id"], datetime(2026, 1, 15, 12, 0), Status.CANCELLED, [(keyboard, 10)]
    )

    return {"mouse": mouse, "keyboard": keyboard}


async def test_sales_report_with_valid_range_excludes_cancelled_orders(
    auth_admin_client: AsyncClient, seeded_sales
):
    # Arrange - 2 pedidos válidos (60 y 131) + 1 cancelado en enero
    params = {"start_date": "2026-01-01", "end_date": "2026-01-31", "granularity": "month"}

    # Act
    response = await auth_admin_client.get("/reports/sales", params=params)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["granularity"] == "month"
    assert data["total_orders"] == 2
    assert Decimal(data["grand_total"]) == Decimal("191.00")
    assert len(data["rows"]) == 1
    row = data["rows"][0]
    assert row["period"].startswith("2026-01-01T00:00:00")
    assert row["orders_count"] == 2
    assert Decimal(row["total_revenue"]) == Decimal("191.00")
    assert Decimal(row["average_ticket"]) == Decimal("95.50")


async def test_sales_report_with_day_granularity_returns_one_row_per_day(
    auth_admin_client: AsyncClient, seeded_sales
):
    params = {"start_date": "2026-01-01", "end_date": "2026-01-31"}

    response = await auth_admin_client.get("/reports/sales", params=params)

    assert response.status_code == 200
    data = response.json()
    assert data["granularity"] == "day"
    assert [row["period"][:10] for row in data["rows"]] == ["2026-01-05", "2026-01-31"]


async def test_sales_report_with_start_date_after_end_date_returns_400(
    auth_admin_client: AsyncClient,
):
    params = {"start_date": "2026-02-01", "end_date": "2026-01-01"}

    response = await auth_admin_client.get("/reports/sales", params=params)

    assert response.status_code == 400


async def test_sales_report_with_range_over_max_days_returns_400(
    auth_admin_client: AsyncClient,
):
    params = {"start_date": "2025-01-01", "end_date": "2026-01-03"}

    response = await auth_admin_client.get("/reports/sales", params=params)

    assert response.status_code == 400


async def test_sales_report_with_invalid_granularity_returns_422(
    auth_admin_client: AsyncClient,
):
    params = {"start_date": "2026-01-01", "end_date": "2026-01-31", "granularity": "year"}

    response = await auth_admin_client.get("/reports/sales", params=params)

    assert response.status_code == 422


async def test_sales_report_with_range_without_orders_returns_empty_rows(
    auth_admin_client: AsyncClient, seeded_sales
):
    params = {"start_date": "2026-02-01", "end_date": "2026-02-28"}

    response = await auth_admin_client.get("/reports/sales", params=params)

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == []
    assert data["total_orders"] == 0
    assert Decimal(data["grand_total"]) == 0


async def test_top_products_report_with_seeded_orders_returns_products_ordered_by_units_sold(
    auth_admin_client: AsyncClient, seeded_sales
):
    # Arrange - mouse 5 uds (3 + 2), keyboard 2 uds; las 10 del pedido cancelado no cuentan
    params = {"start_date": "2026-01-01", "end_date": "2026-01-31"}

    # Act
    response = await auth_admin_client.get("/reports/top-products", params=params)

    # Assert
    assert response.status_code == 200
    rows = response.json()["rows"]
    assert len(rows) == 2
    assert rows[0]["product_id"] == str(seeded_sales["mouse"].id)
    assert rows[0]["product_name"] == "Wireless Mouse"
    assert rows[0]["units_sold"] == 5
    assert Decimal(rows[0]["revenue"]) == Decimal("100.00")
    assert rows[1]["product_id"] == str(seeded_sales["keyboard"].id)
    assert rows[1]["units_sold"] == 2
    assert Decimal(rows[1]["revenue"]) == Decimal("91.00")


async def test_top_products_report_with_limit_one_returns_single_row(
    auth_admin_client: AsyncClient, seeded_sales
):
    params = {"start_date": "2026-01-01", "end_date": "2026-01-31", "limit": 1}

    response = await auth_admin_client.get("/reports/top-products", params=params)

    assert response.status_code == 200
    rows = response.json()["rows"]
    assert len(rows) == 1
    assert rows[0]["product_name"] == "Wireless Mouse"


async def test_top_products_report_with_limit_over_max_returns_422(
    auth_admin_client: AsyncClient,
):
    params = {"start_date": "2026-01-01", "end_date": "2026-01-31", "limit": 51}

    response = await auth_admin_client.get("/reports/top-products", params=params)

    assert response.status_code == 422


async def test_low_stock_report_with_threshold_returns_only_products_at_or_below_it(
    auth_admin_client: AsyncClient, db_session: AsyncSession, created_category: dict
):
    # Arrange
    low_stock_product = await seed_product(db_session, created_category["id"], "USB Cable", 5, 2)
    await seed_product(db_session, created_category["id"], "Monitor", 150, 20)

    # Act
    response = await auth_admin_client.get("/reports/low-stock", params={"threshold": 5})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 5
    assert data["total_products"] == 1
    assert data["rows"] == [
        {
            "product_id": str(low_stock_product.id),
            "product_name": "USB Cable",
            "category_name": created_category["name"],
            "stock": 2,
        }
    ]


async def test_low_stock_report_with_negative_threshold_returns_422(
    auth_admin_client: AsyncClient,
):
    response = await auth_admin_client.get("/reports/low-stock", params={"threshold": -1})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "url",
    [
        "/reports/sales?start_date=2026-01-01&end_date=2026-01-31",
        "/reports/top-products?start_date=2026-01-01&end_date=2026-01-31",
        "/reports/low-stock",
    ],
)
async def test_report_without_authentication_returns_401(client: AsyncClient, url: str):
    response = await client.get(url)

    assert response.status_code == 401


async def test_report_without_admin_role_returns_403(auth_client: AsyncClient):
    response = await auth_client.get("/reports/low-stock")

    assert response.status_code == 403

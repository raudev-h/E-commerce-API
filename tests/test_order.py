import pytest
from httpx import AsyncClient
from sqlalchemy import select
from models import Order, Status, Product, CartItem


async def test_get_orders_returns_list(auth_user_client: AsyncClient, created_order):
    # Arrange - orden ya existe en DB para el usuario autenticado

    # Act
    response = await auth_user_client.get("/order/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(order["id"] == created_order["id"] for order in data)


async def test_get_order_with_different_user(auth_client: AsyncClient, created_order):
    # Arrange - admin intenta obtener una orden que pertenece a otro usuario
    order_id = created_order["id"]

    # Act
    response = await auth_client.get(f"/order/{order_id}")

    # Assert
    assert response.status_code == 404


async def test_get_order_by_id(auth_user_client: AsyncClient, created_order):
    # Arrange
    order_id = created_order["id"]

    # Act
    response = await auth_user_client.get(f"/order/{order_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["user_id"] == created_order["user_id"]
    assert data["total"] == created_order["total"]


async def test_get_order_with_wrong_id(auth_user_client: AsyncClient):
    # Arrange - UUID válido pero sin orden asociada

    # Act
    response = await auth_user_client.get("/order/00000000-0000-0000-0000-000000000000")

    # Assert
    assert response.status_code == 404


async def test_create_order(auth_user_client: AsyncClient, created_cart_item):
    # Arrange
    expected_total = created_cart_item["quantity"] * created_cart_item["price"]

    # Act
    response = await auth_user_client.post("/order/")

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["total"] == expected_total


async def test_create_order_without_auth(client: AsyncClient):
    # Arrange - sin token

    # Act
    response = await client.post("/order/")

    # Assert
    assert response.status_code == 401

async def test_create_order_with_empty_cart(auth_user_client:AsyncClient):
    response = await auth_user_client.post("/order/")
    assert response.status_code == 409

async def test_cancel_order(auth_user_client:AsyncClient, created_order):
    response = await auth_user_client.patch(f"/order/{created_order["id"]}")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "canceled"

async def test_cancel_order_with_wrong_id(auth_user_client:AsyncClient, created_order):
    response = await auth_user_client.patch("/order/00000000-0000-0000-0000-000000000000")
    
    assert response.status_code == 404
    assert created_order["status"] == "pending"

async def test_cancel_order_when_order_belongs_to_other_user(auth_client:AsyncClient, created_order):
    response = await auth_client.patch(f"/order/{created_order["id"]}")

    assert response.status_code == 404

async def test_cancel_order_without_been_cancellable(auth_user_client:AsyncClient, db_session, created_order):
    order = await db_session.execute(select(Order).where(Order.id == created_order["id"]))
    order = order.scalar_one_or_none()
    order.status = Status.DELIVERED

    await db_session.flush()

    response = await auth_user_client.patch(f"/order/{created_order["id"]}")
    assert response.status_code == 400

    order = await db_session.execute(select(Order).where(Order.id == created_order["id"]))
    order = order.scalar_one_or_none()
    assert  order.status == Status.DELIVERED

async def test_verify_empty_cart_after_order_and_stock_deduct_correctly(auth_user_client:AsyncClient, db_session, created_cart_item):
    product = await db_session.execute(select(Product).where(Product.id == created_cart_item["product_id"]))
    product = product.scalar_one_or_none()
    expected_stock = product.stock - created_cart_item["quantity"]

    response = await auth_user_client.post("/order/")

    product = await db_session.execute(select(Product).where(Product.id == created_cart_item["product_id"]))
    product = product.scalar_one_or_none()
    
    assert response.status_code == 201
    assert product.stock == expected_stock

    cart_items = await db_session.execute(select(CartItem).where(CartItem.cart_id == created_cart_item["cart_id"]))
    cart_items = cart_items.scalars().all()
    assert cart_items == []

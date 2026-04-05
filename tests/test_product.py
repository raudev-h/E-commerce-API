import pytest
from httpx import AsyncClient
from uuid import uuid4


async def test_get_all_products(client: AsyncClient):
    response = await client.get("/product/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_product_by_id(client: AsyncClient, created_product):
    product_id = created_product["id"]
    response = await client.get(f"/product/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == created_product["name"]


async def test_get_product_wiht_wrong_id(client: AsyncClient, created_product):
    response = await client.get("/product/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


async def test_create_product(auth_admin_client: AsyncClient, created_category):
    product_data = {
        "name": "iPhone 12 Pro Max",
        "description": "2021 Apple smartphone",
        "price": 300,
        "stock": 10,
        "category_id": created_category["id"],
    }
    response = await auth_admin_client.post("/product/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["category_id"] == product_data["category_id"]
    assert data["is_active"] == True
    assert "smartphone" in data["description"]


async def test_create_duplicate_product(
    auth_admin_client: AsyncClient, created_product
):
    product_data = {
        "name": "iPhone 12 Pro Max",
        "description": "2021 Apple smartphone",
        "price": 300,
        "stock": 10,
        "category_id": created_product["category_id"],
    }
    response = await auth_admin_client.post("/product/", json=product_data)
    assert response.status_code == 409


async def test_create_product_without_been_admin(
    auth_client: AsyncClient, created_category
):
    product_data = {
        "name": "iPhone 12 Pro Max",
        "description": "2021 Apple smartphone",
        "price": 300,
        "stock": 10,
        "category_id": created_category["id"],
    }
    response = await auth_client.post("/product/", json=product_data)
    assert response.status_code == 403


async def test_create_product_with_wrong_category_id(auth_admin_client: AsyncClient):
    product_data = {
        "name": "iPhone 12 Pro Max",
        "description": "2021 Apple smartphone",
        "price": 300,
        "stock": 10,
        "category_id": str(uuid4()),
    }
    response = await auth_admin_client.post("/product/", json=product_data)
    assert response.status_code == 404

    response = await auth_admin_client.get("/product/")
    products = response.json()
    assert not any(p["name"] == product_data["name"] for p in products)


async def test_update_product(auth_admin_client: AsyncClient, created_product):
    updated_data = {
        "name": "iPhone 14 Pro Max",
        "description": "iphone latest release",
        "stock": 4,
    }
    response = await auth_admin_client.patch(
        f"/product/{created_product["id"]}", json=updated_data
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]
    assert data["stock"] == updated_data["stock"]
    assert data["price"] == created_product["price"]


async def test_update_product_without_been_admin(auth_client: AsyncClient, created_product):
    updated_data = {"name": "iPhone 14 Pro Max"}

    response = await auth_client.patch(f"/product/{created_product["id"]}", json=updated_data)
    assert response.status_code == 403

async def test_soft_delete(auth_admin_client:AsyncClient, created_product):
    response = await auth_admin_client.delete(f"/product/{created_product["id"]}")
    assert response.status_code == 204

    response = await auth_admin_client.get(f"/product/{created_product["id"]}")
    assert response.status_code == 404
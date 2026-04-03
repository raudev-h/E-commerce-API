import pytest
from httpx import AsyncClient

'''
crear un producto con un category_id inexistente
actualizar un producto (cambiar description, nombre, stock) comprobar que solo cambiaron los campos concretos
actualizar un producto isn ser admin
soft delete -> is_active = False
hacer get de un producto eliminado -> 404
'''

async def test_get_all_products(client:AsyncClient):
    response = await client.get("/product/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_get_product_by_id(client:AsyncClient, created_product):
    product_id = created_product["id"]
    response = await client.get(f"/product/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == created_product["name"]

async def test_get_product_wiht_wrong_id(client:AsyncClient, created_product):
    response = await client.get("/product/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

async def test_create_product(auth_admin_client:AsyncClient, created_category):
    product_data = {
        "name":"iPhone 12 Pro Max",
        "description":"2021 Apple smartphone",
        "price":300,
        "stock":10,
        "category_id":created_category["id"]
    }
    response = await auth_admin_client.post("/product/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["category_id"] == product_data["category_id"]
    assert data["is_active"] == True
    assert "smartphone" in data["description"]

async def test_create_duplicate_product(auth_admin_client:AsyncClient, created_product):
    product_data = {
        "name":"iPhone 12 Pro Max",
        "description":"2021 Apple smartphone",
        "price":300,
        "stock":10,
        "category_id":created_product["category_id"]
    }
    response = await auth_admin_client.post("/product/", json=product_data)
    assert response.status_code == 409

async def test_create_product_without_been_admin(auth_client:AsyncClient, created_category):
    product_data = {
        "name":"iPhone 12 Pro Max",
        "description":"2021 Apple smartphone",
        "price":300,
        "stock":10,
        "category_id":created_category["id"]
    }
    response = await auth_client.post("/product/", json=product_data)
    assert response.status_code == 403
import pytest
from .conftest import CATEGORY_DATA
from httpx import AsyncClient
from models import Category


async def test_get_all_categories(client:AsyncClient):
    response = await client.get("/category/")
    assert response.status_code == 200
    assert isinstance(response.json(),list)

async def test_get_category_by_id(client:AsyncClient, created_category:dict):
    category_id = created_category["id"]
    response = await client.get(f"/category/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == created_category["name"]

async def test_get_category_with_wrong_id(client:AsyncClient):
    response = await client.get("/category/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

async def test_create_category(auth_admin_client:AsyncClient):
    new_category = {"name":"Deporte","description": "sport articles"}
    response = await auth_admin_client.post("/category/", json=new_category)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_category["name"]
    assert data["description"] == new_category["description"]
    assert data["is_active"] == True
    assert "id" in data

async def  test_create_duplicate_category(auth_admin_client:AsyncClient, created_category):
    response = await auth_admin_client.post("/category/", json=CATEGORY_DATA)
    assert response.status_code == 409

async def test_create_category_without_been_admin(auth_client:AsyncClient):
    response = await auth_client.post("/category/", json=CATEGORY_DATA)
    assert response.status_code == 403

async def test_update_category(auth_admin_client:AsyncClient, created_category):
    category_id = created_category["id"]
    updated_category_description = {"description":"technology articles"}
    response = await auth_admin_client.patch(f"/category/{category_id}", json=updated_category_description)
    assert response.status_code == 200

async def test_soft_delete_category(auth_admin_client:AsyncClient, created_category):
    category_id = created_category["id"]
    response = await auth_admin_client.delete(f"/category/{category_id}")
    assert response.status_code == 204
    
    response = await auth_admin_client.get(f"/category/{category_id}")
    assert response.status_code == 404
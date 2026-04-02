import pytest
from .conftest import USER_DATA
from httpx import AsyncClient



async def test_create_user(client:AsyncClient):
    response = await client.post("/user/",json=USER_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == USER_DATA["email"]
    assert data["first_name"] == USER_DATA["first_name"]
    assert "password" not in data

async def test_create_duplicate_user(client:AsyncClient):
    await client.post("/user/", json=USER_DATA)

    response = await client.post("/user/", json=USER_DATA)

    assert response.status_code == 409

async def test_create_user_with_short_password(client:AsyncClient):
    short_pwd_data = {**USER_DATA, "password":"123", "confirm_password":"123"}
    response = await client.post("/user/", json=short_pwd_data)
    assert response.status_code == 422

async def test_create_user_without_confirm_password(client:AsyncClient):
    no_confirm_data = USER_DATA.copy()
    del no_confirm_data["confirm_password"]
    response = await client.post("/user/", json=no_confirm_data)
    assert response.status_code == 422
import pytest
from httpx import AsyncClient


USER_DATA = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test@test.com",
    "password": "password123",
    "confirm_password": "password123"
}

async def test_create_user(client:AsyncClient):
    response = await client.post("/user/",json=USER_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == USER_DATA["email"]
    assert data["first_name"] == USER_DATA["first_name"]
    assert "password" not in data
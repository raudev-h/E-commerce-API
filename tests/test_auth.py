import pytest
from .conftest import USER_DATA
from httpx import AsyncClient

async def test_login_wrong_password(client:AsyncClient):
    await client.post("/user/", json=USER_DATA)
    response = await client.post("/auth/login", data={"username":USER_DATA["email"], "password":"wrongpassword"})
    assert response.status_code == 401

async def test_successfull_login(client:AsyncClient):
    await client.post("/user/", json=USER_DATA)
    response = await client.post("/auth/login", data={"username":USER_DATA["email"], "password":USER_DATA["password"]})
    assert response.status_code == 200
import pytest
from sqlalchemy import select
from .conftest import USER_DATA
from httpx import AsyncClient
from models import User


async def test_login_wrong_password(client:AsyncClient):
    await client.post("/user/", json=USER_DATA)
    response = await client.post("/auth/login", data={"username":USER_DATA["email"], "password":"wrongpassword"})
    assert response.status_code == 401

async def test_successfull_login(client:AsyncClient):
    await client.post("/user/", json=USER_DATA)
    response = await client.post("/auth/login", data={"username":USER_DATA["email"], "password":USER_DATA["password"]})
    assert response.status_code == 200

async def test_login_with_inactive_user(db_session, created_user, client:AsyncClient):
    user = await db_session.execute(select(User).where(User.id == created_user["id"]))
    user = user.scalar_one_or_none()
    user.is_active = False

    await db_session.flush()

    response = await client.post("/auth/login", data={"username":created_user["email"], "password":created_user["password"]})

    assert response.status_code == 401
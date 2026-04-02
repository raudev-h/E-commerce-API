import pytest
import pytest_asyncio
from models import User,UserRole
from core.config import settings
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from main import app
from core.database import Base, get_db

USER_DATA = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test@test.com",
    "password": "password123",
    "confirm_password": "password123",
}

ADMIN_DATA = {
    "first_name": "Admin",
    "last_name": "Admin",
    "email": "admin@test.com",
    "password": "password123",
    "confirm_password": "password123",
}

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    test_engine = create_async_engine(settings.test_database_url, echo=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_database):
    engine = setup_database
    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient):
    await client.post("/user/", json=USER_DATA)
    response = await client.post(
        "/auth/login",
        data={"username": USER_DATA["email"], "password": USER_DATA["password"]},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client

@pytest_asyncio.fixture
async def auth_admin_client(client:AsyncClient, db_session):
    await client.post("/user/", json=ADMIN_DATA)
    result = await db_session.execute(select(User).where(User.email == ADMIN_DATA["email"]))
    user:User = result.scalar_one()
    user.role = UserRole.admin
    await db_session.flush()
    response = await client.post(
        "/auth/login",
        data={"username": ADMIN_DATA["email"], "password": ADMIN_DATA["password"]},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
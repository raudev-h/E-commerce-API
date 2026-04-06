import pytest
import pytest_asyncio
from models import User, UserRole, Category, Product, CartItem, Cart, Order, OrderItem, Status
from core.config import settings
from core.security import get_password_hash
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

CATEGORY_DATA = {"name": "Tech", "description": "tech articles"}


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
async def auth_admin_client(client: AsyncClient, db_session):
    await client.post("/user/", json=ADMIN_DATA)
    result = await db_session.execute(
        select(User).where(User.email == ADMIN_DATA["email"])
    )
    user: User = result.scalar_one()
    user.role = UserRole.admin
    await db_session.flush()
    response = await client.post(
        "/auth/login",
        data={"username": ADMIN_DATA["email"], "password": ADMIN_DATA["password"]},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest_asyncio.fixture
async def created_category(db_session):
    category = Category(name="Tech", description="tech articles")
    db_session.add(category)
    await db_session.flush()
    await db_session.refresh(category)
    return {
        "id": str(category.id),
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
    }


@pytest_asyncio.fixture
async def created_product(db_session, created_category: dict):
    product = Product(
        name="iPhone 12 Pro Max",
        description="2021 Apple smartphone",
        price=300,
        stock=10,
        category_id=created_category["id"],
    )
    db_session.add(product)
    await db_session.flush()
    await db_session.refresh(product)

    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category_id": str(product.category_id),
        "is_active": product.is_active,
    }

@pytest_asyncio.fixture
async def created_user(db_session):
    user = User(
        first_name= "Test",
        last_name= "User",
        email= "user@test.com",
        password= get_password_hash("password123"),
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    cart = Cart(
        user_id=user.id,
    )
    db_session.add(cart)
    await db_session.flush()
    await db_session.refresh(cart)

    return {
        "id":str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "cart_id":cart.id
    }

@pytest_asyncio.fixture
async def auth_user_client(client: AsyncClient, created_user):
    response = await client.post(
        "/auth/login",
        data={"username": created_user["email"], "password": "password123"},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest_asyncio.fixture
async def created_cart_item(db_session, created_user, created_product):    
    cart_id = created_user["cart_id"]
    cart_item = CartItem(
        cart_id=cart_id,
        product_id=created_product["id"],
        quantity=2
    )
    db_session.add(cart_item)
    await db_session.flush()
    await db_session.refresh(cart_item)

    return{
        "id": str(cart_item.id),
        "cart_id": str(cart_id),
        "product_id": created_product["id"],
        "quantity": cart_item.quantity,
        "updated_at": cart_item.updated_at,
        "price":created_product["price"]
    }

@pytest_asyncio.fixture
async def created_oder(db_session, created_user, created_cart_item):
    total_price = created_cart_item["quantity"] * created_cart_item["price"]
    order = Order(
        user_id=created_user["id"],
        total=total_price,
        status=Status.PENDING
    )
    db_session.add(order)
    await db_session.flush()
    await db_session.refresh(order)

    order_item = OrderItem(
        order_id=str(order.id),
        product_id=str(created_cart_item["product_id"]),
        quantity=created_cart_item["quantity"],
        unit_price= created_cart_item["price"]
    )
    db_session.add(order_item)
    await db_session.flush()

    return {
        "id":str(order.id),
        "user_id":str(order.user_id),
        "total":order.total,
        "status":order.status
    }
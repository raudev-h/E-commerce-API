import pytest
from httpx import AsyncClient

'''
Casos De Prueba
1-obtener todas las ordenes y que devuelva una lista
2-intentar obtener las ordenes con el user_id incorrecto
3-obtener una orden por id
4-obtener una orden con id incorrecto
5-crear una orden
6-crear una orden con user_id incorrecto
7-crear una orden de un usuario inactivo
8-crear una orden con el carrito vacío
9-cancelar una orden
10-cancelar una orden con order_id incorrecto
11-cancelar una orden con user_id incorrecto
12-cancelar una orden sin cancellable status
13-Verificar que el stock se descuenta correctamente al crear una orden
14-Verificar que el carrito queda vacío después de crear la orden
'''


async def test_get_orders_returns_list(auth_user_client: AsyncClient, created_oder):
    # Arrange - orden ya existe en DB para el usuario autenticado

    # Act
    response = await auth_user_client.get("/order/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(order["id"] == created_oder["id"] for order in data)


async def test_get_order_with_different_user(auth_client: AsyncClient, created_oder):
    # Arrange - admin intenta obtener una orden que pertenece a otro usuario
    order_id = created_oder["id"]

    # Act
    response = await auth_client.get(f"/order/{order_id}")

    # Assert
    assert response.status_code == 404


async def test_get_order_by_id(auth_user_client: AsyncClient, created_oder):
    # Arrange
    order_id = created_oder["id"]

    # Act
    response = await auth_user_client.get(f"/order/{order_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["user_id"] == created_oder["user_id"]
    assert data["total"] == created_oder["total"]


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

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product():
    """Test para crear un producto"""
    product_data = {
        "name": "Laptop",
        "product_type": "Electronics",
        "list_price": 15000.00
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["product_type"] == product_data["product_type"]
    # MySQL guarda con 2 decimales, por eso esperamos '15000.00' en lugar de '15000.0'
    assert data["list_price"] == "15000.00"

def test_get_products():
    """Test para obtener todos los productos"""
    response = client.get("/products/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # Verificar que al menos hay un producto (el que creamos en el test anterior)
    assert len(data) > 0

def test_create_product_invalid_price():
    """Test para validar precio inválido"""
    product_data = {
        "name": "Invalid Product",
        "product_type": "Electronics",
        "list_price": -100.00  # Precio negativo
    }

    response = client.post("/products/", json=product_data)
    # La API devuelve 422 Unprocessable Entity para validación de datos
    assert response.status_code == 422

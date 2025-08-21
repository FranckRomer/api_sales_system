import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product_discount():
    """Test para crear un descuento por tipo de producto"""
    discount_data = {
        "product_type": "Electronics",
        "discount_percent": 5.0
    }

    response = client.post("/discounts/product", json=discount_data)
    assert response.status_code == 201

    data = response.json()
    assert data["product_type"] == discount_data["product_type"]
    # MySQL guarda con 2 decimales, por eso esperamos '5.00' en lugar de '5.0'
    assert data["discount_percent"] == "5.00"

def test_create_payment_discount():
    """Test para crear un descuento por método de pago"""
    discount_data = {
        "payment_method": "Cash",
        "discount_percent": 5.0
    }

    response = client.post("/discounts/payment", json=discount_data)
    assert response.status_code == 201

    data = response.json()
    assert data["payment_method"] == discount_data["payment_method"]
    # MySQL guarda con 2 decimales, por eso esperamos '5.00' en lugar de '5.0'
    assert data["discount_percent"] == "5.00"

def test_create_discount_invalid_percent():
    """Test para validar descuento con porcentaje inválido"""
    discount_data = {
        "product_type": "Electronics",
        "discount_percent": 150.0  # Más del 100%
    }

    response = client.post("/discounts/product", json=discount_data)
    # La API devuelve 422 Unprocessable Entity para validación de datos
    assert response.status_code == 422

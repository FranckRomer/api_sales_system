import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_sale():
    """Test para crear una venta"""
    # Crear un cliente primero
    customer_data = {
        "name": "Test Customer",
        "customer_type": "VIP",
        "credit_terms_days": 90
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["customer_id"]

    # Crear un producto primero
    product_data = {
        "name": "Test Product",
        "product_type": "Electronics",
        "list_price": 1000.00
    }
    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["product_id"]

    # Crear la venta
    sale_data = {
        "customer_id": customer_id,
        "payment_method": "Cash",
        "items": [{"product_id": product_id, "quantity": 2}]
    }

    response = client.post("/sales/", json=sale_data)
    assert response.status_code == 201

    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["payment_method"] == "Cash"
    # MySQL guarda con 2 decimales, por eso esperamos '16.00' en lugar de 16.0
    assert data["tax_rate_percent"] == "16.00"
    assert "breakdown" in data
    # Convertir el total a float para poder comparar numéricamente
    assert float(data["breakdown"]["total"]) > 0

def test_get_sales():
    """Test para obtener todas las ventas"""
    response = client.get("/sales/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # Verificar que al menos hay una venta (la que creamos en el test anterior)
    assert len(data) > 0

def test_create_sale_invalid_customer():
    """Test para validar cliente inexistente"""
    sale_data = {
        "customer_id": 99999,  # Cliente que no existe
        "payment_method": "Cash",
        "items": [{"product_id": 1, "quantity": 1}]
    }

    response = client.post("/sales/", json=sale_data)
    # La API devuelve 400 Bad Request en lugar de 404 Not Found
    assert response.status_code == 400

def test_create_sale_invalid_product():
    """Test para validar producto inexistente"""
    # Crear un cliente primero
    customer_data = {
        "name": "Test Customer 2",
        "customer_type": "Regular",
        "credit_terms_days": 30
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["customer_id"]

    sale_data = {
        "customer_id": customer_id,
        "payment_method": "Cash",
        "items": [{"product_id": 99999, "quantity": 1}]  # Producto que no existe
    }

    response = client.post("/sales/", json=sale_data)
    # La API devuelve 400 Bad Request en lugar de 404 Not Found
    assert response.status_code == 400

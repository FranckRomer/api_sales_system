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
    assert data["list_price"] == str(product_data["list_price"])  # Decimal se serializa como string

def test_get_products():
    """Test para obtener todos los productos"""
    response = client.get("/products/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Debería tener al menos el producto creado

def test_create_product_invalid_price():
    """Test para validar precio inválido"""
    product_data = {
        "name": "Test Product",
        "product_type": "Test",
        "list_price": -100  # Precio negativo
    }
    
    response = client.post("/products/", json=product_data)
    assert response.status_code == 422  # Validation error

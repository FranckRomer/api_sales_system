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
    assert data["discount_percent"] == str(discount_data["discount_percent"])  # Decimal se serializa como string

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
    assert data["discount_percent"] == str(discount_data["discount_percent"])  # Decimal se serializa como string

def test_create_discount_invalid_percent():
    """Test para validar porcentaje de descuento inválido"""
    discount_data = {
        "product_type": "Test",
        "discount_percent": 150  # Más de 100%
    }
    
    response = client.post("/discounts/product", json=discount_data)
    assert response.status_code == 422  # Validation error

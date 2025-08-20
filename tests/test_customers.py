from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_customer():
    """Test para crear un cliente"""
    customer_data = {
        "name": "Ana",
        "customer_type": "VIP",
        "credit_terms_days": 90
    }
    
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["customer_type"] == customer_data["customer_type"]
    assert data["credit_terms_days"] == customer_data["credit_terms_days"]
    assert "customer_id" in data

def test_create_customer_regular():
    """Test para crear un cliente regular"""
    customer_data = {
        "name": "Luis",
        "customer_type": "Regular",
        "credit_terms_days": 30
    }
    
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["customer_type"] == "Regular"
    assert data["credit_terms_days"] == 30

def test_get_customers():
    """Test para obtener todos los clientes"""
    response = client.get("/customers/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Debería tener al menos los 2 clientes creados

def test_create_customer_invalid_type():
    """Test para validar tipo de cliente inválido"""
    customer_data = {
        "name": "Test User",
        "customer_type": "Invalid",
        "credit_terms_days": 30
    }
    
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 422  # Validation error

def test_create_customer_invalid_credit_terms():
    """Test para validar términos de crédito inválidos"""
    customer_data = {
        "name": "Test User",
        "customer_type": "VIP",
        "credit_terms_days": 400  # Más de 365 días
    }
    
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 422  # Validation error

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_sale():
    """Test para crear una venta"""
    # Primero crear un cliente y producto para la venta
    customer_data = {
        "name": "Test Customer",
        "customer_type": "VIP",
        "credit_terms_days": 90
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["customer_id"]
    
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
        "payment_method": "Store Credit",
        "items": [{"product_id": product_id, "quantity": 1}]
    }
    
    response = client.post("/sales/", json=sale_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["payment_method"] == sale_data["payment_method"]
    assert "sale_id" in data
    assert "breakdown" in data
    assert float(data["breakdown"]["total"]) > 0  # Convertir string a float para comparar

def test_get_sales():
    """Test para obtener todas las ventas"""
    response = client.get("/sales/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Debería tener al menos la venta creada

def test_create_sale_invalid_customer():
    """Test para validar cliente inexistente"""
    sale_data = {
        "customer_id": 99999,  # Cliente que no existe
        "payment_method": "Cash",
        "items": [{"product_id": 1, "quantity": 1}]
    }
    
    response = client.post("/sales/", json=sale_data)
    assert response.status_code == 404  # Not found

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
    assert response.status_code == 404  # Not found

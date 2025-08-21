#!/usr/bin/env python3
"""
Script para inicializar la base de datos
Ejecutar: python database/init_database.py
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database.connection import create_tables, engine
from app.database.models import *
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

def init_database():
    """Inicializar la base de datos con datos básicos"""
    
    print("🔄 Creando tablas...")
    create_tables()
    print("✅ Tablas creadas exitosamente")
    
    # Crear sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🔄 Insertando datos básicos...")
        
        # Verificar si ya existen datos
        existing_customer_types = db.query(CustomerType).count()
        if existing_customer_types > 0:
            print("⚠️  La base de datos ya contiene datos. Saltando inserción...")
            return
        
        # Insertar tipos de cliente
        customer_types = [
            CustomerType(name="VIP"),
            CustomerType(name="Regular")
        ]
        db.add_all(customer_types)
        db.flush()
        
        # Insertar términos de crédito
        credit_terms = [
            CreditTerms(days=30),
            CreditTerms(days=60),
            CreditTerms(days=90),
            CreditTerms(days=120),
            CreditTerms(days=180),
            CreditTerms(days=365)
        ]
        db.add_all(credit_terms)
        db.flush()
        
        # Insertar tipos de producto
        product_types = [
            ProductType(name="Electronics"),
            ProductType(name="Clothing"),
            ProductType(name="Books"),
            ProductType(name="Home & Garden"),
            ProductType(name="Sports"),
            ProductType(name="Automotive")
        ]
        db.add_all(product_types)
        db.flush()
        
        # Insertar métodos de pago
        payment_methods = [
            PaymentMethod(name="Cash"),
            PaymentMethod(name="Credit Card"),
            PaymentMethod(name="Debit Card"),
            PaymentMethod(name="Store Credit"),
            PaymentMethod(name="Bank Transfer"),
            PaymentMethod(name="Digital Wallet")
        ]
        db.add_all(payment_methods)
        db.flush()
        
        # Insertar descuentos por tipo de producto
        product_discounts = [
            ProductTypeDiscount(product_type_id=1, discount_percent=Decimal('5.00')),  # Electronics: 5%
            ProductTypeDiscount(product_type_id=2, discount_percent=Decimal('10.00')), # Clothing: 10%
            ProductTypeDiscount(product_type_id=3, discount_percent=Decimal('15.00')), # Books: 15%
            ProductTypeDiscount(product_type_id=4, discount_percent=Decimal('8.00')),  # Home & Garden: 8%
            ProductTypeDiscount(product_type_id=5, discount_percent=Decimal('12.00')), # Sports: 12%
            ProductTypeDiscount(product_type_id=6, discount_percent=Decimal('7.00'))   # Automotive: 7%
        ]
        db.add_all(product_discounts)
        db.flush()
        
        # Insertar descuentos por método de pago
        payment_discounts = [
            PaymentMethodDiscount(payment_method_id=1, discount_percent=Decimal('5.00')),  # Cash: 5%
            PaymentMethodDiscount(payment_method_id=2, discount_percent=Decimal('2.00')), # Credit Card: 2%
            PaymentMethodDiscount(payment_method_id=3, discount_percent=Decimal('3.00')), # Debit Card: 3%
            PaymentMethodDiscount(payment_method_id=4, discount_percent=Decimal('1.90')), # Store Credit: 1.9%
            PaymentMethodDiscount(payment_method_id=5, discount_percent=Decimal('0.00')), # Bank Transfer: 0%
            PaymentMethodDiscount(payment_method_id=6, discount_percent=Decimal('4.00'))  # Digital Wallet: 4%
        ]
        db.add_all(payment_discounts)
        db.flush()
        
        # Insertar clientes de ejemplo
        customers = [
            Customer(name="Ana García", customer_type_id=1, credit_terms_id=3),      # VIP con 90 días
            Customer(name="Luis Rodríguez", customer_type_id=2, credit_terms_id=1),  # Regular con 30 días
            Customer(name="María López", customer_type_id=1, credit_terms_id=4),     # VIP con 120 días
            Customer(name="Carlos Pérez", customer_type_id=2, credit_terms_id=2)     # Regular con 60 días
        ]
        db.add_all(customers)
        db.flush()
        
        # Insertar productos de ejemplo
        products = [
            Product(name="Laptop Gaming", product_type_id=1, list_price=Decimal('15000.00')),
            Product(name="Smartphone", product_type_id=1, list_price=Decimal('8000.00')),
            Product(name="Camiseta Casual", product_type_id=2, list_price=Decimal('500.00')),
            Product(name="Libro de Programación", product_type_id=3, list_price=Decimal('800.00')),
            Product(name="Mesa de Oficina", product_type_id=4, list_price=Decimal('2500.00')),
            Product(name="Balón de Fútbol", product_type_id=5, list_price=Decimal('300.00'))
        ]
        db.add_all(products)
        db.flush()
        
        # Commit de todos los cambios
        db.commit()
        print("✅ Datos básicos insertados exitosamente")
        
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando base de datos...")
    init_database()
    print("🎉 Base de datos inicializada exitosamente!")

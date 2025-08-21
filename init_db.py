#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos básicos
"""
import asyncio
from sqlalchemy.orm import Session
from app.database.connection import get_db, create_tables
from app.repositories.customer_type_repository import CustomerTypeRepository
from app.repositories.credit_terms_repository import CreditTermsRepository
from app.repositories.product_type_repository import ProductTypeRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.credit_terms_discount_repository import CreditTermsDiscountRepository

def init_database():
    """Inicializar la base de datos con datos básicos"""
    print("🚀 Inicializando base de datos...")
    
    # Crear tablas
    create_tables()
    print("✅ Tablas creadas")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Crear tipos de cliente
        customer_type_repo = CustomerTypeRepository()
        customer_types = [
            {"name": "VIP"},
            {"name": "Regular"}
        ]
        
        for ct_data in customer_types:
            existing = customer_type_repo.get_by_name(db, ct_data["name"])
            if not existing:
                customer_type_repo.create(db, ct_data)
                print(f"✅ Tipo de cliente creado: {ct_data['name']}")
            else:
                print(f"ℹ️  Tipo de cliente ya existe: {ct_data['name']}")
        
        # 2. Crear términos de crédito
        credit_terms_repo = CreditTermsRepository()
        credit_terms = [
            {"days": 30},
            {"days": 90},
            {"days": 120}
        ]
        
        for ct_data in credit_terms:
            existing = credit_terms_repo.get_by_days(db, ct_data["days"])
            if not existing:
                credit_terms_repo.create(db, ct_data)
                print(f"✅ Términos de crédito creados: {ct_data['days']} días")
            else:
                print(f"ℹ️  Términos de crédito ya existen: {ct_data['days']} días")
        
        # 3. Crear tipos de producto
        product_type_repo = ProductTypeRepository()
        product_types = [
            {"name": "Electronics"},
            {"name": "Clothing"},
            {"name": "Books"}
        ]
        
        for pt_data in product_types:
            existing = product_type_repo.get_by_name(db, pt_data["name"])
            if not existing:
                product_type_repo.create(db, pt_data)
                print(f"✅ Tipo de producto creado: {pt_data['name']}")
            else:
                print(f"ℹ️  Tipo de producto ya existe: {pt_data['name']}")
        
        # 4. Crear métodos de pago
        payment_method_repo = PaymentMethodRepository()
        payment_methods = [
            {"name": "Cash"},
            {"name": "Credit Card"},
            {"name": "Store Credit"}
        ]
        
        for pm_data in payment_methods:
            existing = payment_method_repo.get_by_name(db, pm_data["name"])
            if not existing:
                payment_method_repo.create(db, pm_data)
                print(f"✅ Método de pago creado: {pm_data['name']}")
            else:
                print(f"ℹ️  Método de pago ya existe: {pm_data['name']}")
        
        # 5. Crear descuentos por términos de crédito (nuevo)
        credit_terms_discount_repo = CreditTermsDiscountRepository()
        
        # Obtener los términos de crédito creados
        credit_terms_30 = credit_terms_repo.get_by_days(db, 30)
        credit_terms_90 = credit_terms_repo.get_by_days(db, 90)
        credit_terms_120 = credit_terms_repo.get_by_days(db, 120)
        
        # Crear descuentos según las reglas de negocio: 30d=0%, 90d=2%, 120d=4%
        credit_terms_discounts = [
            {"credit_terms_id": credit_terms_30.credit_terms_id, "discount_percent": 0.0},
            {"credit_terms_id": credit_terms_90.credit_terms_id, "discount_percent": 2.0},
            {"credit_terms_id": credit_terms_120.credit_terms_id, "discount_percent": 4.0}
        ]
        
        for ctd_data in credit_terms_discounts:
            existing = credit_terms_discount_repo.get_by_credit_terms_id(db, ctd_data["credit_terms_id"])
            if not existing:
                credit_terms_discount_repo.create(db, ctd_data)
                print(f"✅ Descuento por términos de crédito creado: {ctd_data['discount_percent']}%")
            else:
                print(f"ℹ️  Descuento por términos de crédito ya existe: {ctd_data['discount_percent']}%")
        
        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📋 Datos creados:")
        print("   - Tipos de cliente: VIP, Regular")
        print("   - Términos de crédito: 30, 90, 120 días")
        print("   - Tipos de producto: Electronics, Clothing, Books")
        print("   - Métodos de pago: Cash, Credit Card, Store Credit")
        print("   - Descuentos por crédito: 30d=0%, 90d=2%, 120d=4%")
        print("\n📊 Reglas de negocio implementadas:")
        print("   - Descuentos secuenciales: Base → ProductType → PaymentMethod → CreditTerms")
        print("   - Solo Store Credit aplica descuento por términos de crédito")
        print("   - Redondeo a 2 decimales en cada línea")
        print("   - Tax 16% sobre subtotal después de descuentos")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()

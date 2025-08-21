from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import ProductTypeDiscount, PaymentMethodDiscount, ProductType, PaymentMethod
from app.repositories.base import BaseRepository

class ProductTypeDiscountRepository(BaseRepository[ProductTypeDiscount]):
    """Repositorio para descuentos por tipo de producto"""
    
    def __init__(self):
        super().__init__(ProductTypeDiscount)
    
    def get_by_product_type(self, db: Session, product_type_id: int) -> Optional[ProductTypeDiscount]:
        """Obtener descuento por tipo de producto"""
        return db.query(ProductTypeDiscount).filter(
            and_(
                ProductTypeDiscount.deleted_at.is_(None),
                ProductTypeDiscount.product_type_id == product_type_id
            )
        ).first()
    
    def get_by_product_type_name(self, db: Session, product_type_name: str) -> Optional[ProductTypeDiscount]:
        """Obtener descuento por nombre del tipo de producto"""
        return db.query(ProductTypeDiscount).join(ProductType).filter(
            and_(
                ProductTypeDiscount.deleted_at.is_(None),
                ProductType.name == product_type_name
            )
        ).first()

class PaymentMethodDiscountRepository(BaseRepository[PaymentMethodDiscount]):
    """Repositorio para descuentos por método de pago"""
    
    def __init__(self):
        super().__init__(PaymentMethodDiscount)
    
    def get_by_payment_method(self, db: Session, payment_method_id: int) -> Optional[PaymentMethodDiscount]:
        """Obtener descuento por método de pago"""
        return db.query(PaymentMethodDiscount).filter(
            and_(
                PaymentMethodDiscount.deleted_at.is_(None),
                PaymentMethodDiscount.payment_method_id == payment_method_id
            )
        ).first()
    
    def get_by_payment_method_name(self, db: Session, payment_method_name: str) -> Optional[PaymentMethodDiscount]:
        """Obtener descuento por nombre del método de pago"""
        return db.query(PaymentMethodDiscount).join(PaymentMethod).filter(
            and_(
                PaymentMethodDiscount.deleted_at.is_(None),
                PaymentMethod.name == payment_method_name
            )
        ).first()

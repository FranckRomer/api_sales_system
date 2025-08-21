from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import Sale, SaleItem
from app.repositories.base import BaseRepository

class SaleRepository(BaseRepository[Sale]):
    """Repositorio para operaciones con ventas"""
    
    def __init__(self):
        super().__init__(Sale)
    
    def get_by_customer(self, db: Session, customer_id: int) -> List[Sale]:
        """Obtener ventas por cliente"""
        return db.query(Sale).filter(
            and_(
                Sale.deleted_at.is_(None),
                Sale.customer_id == customer_id
            )
        ).all()
    
    def get_by_date_range(self, db: Session, start_date, end_date) -> List[Sale]:
        """Obtener ventas por rango de fechas"""
        return db.query(Sale).filter(
            and_(
                Sale.deleted_at.is_(None),
                Sale.sale_datetime >= start_date,
                Sale.sale_datetime <= end_date
            )
        ).all()
    
    def get_with_items(self, db: Session, sale_id: int) -> Optional[Sale]:
        """Obtener venta con sus items"""
        return db.query(Sale).filter(
            and_(
                Sale.deleted_at.is_(None),
                Sale.sale_id == sale_id
            )
        ).first()
    
    def get_total_sales(self, db: Session) -> float:
        """Obtener total de ventas"""
        result = db.query(Sale).filter(
            Sale.deleted_at.is_(None)
        ).with_entities(
            db.func.sum(Sale.total)
        ).scalar()
        return float(result) if result else 0.0

class SaleItemRepository(BaseRepository[SaleItem]):
    """Repositorio para items de venta"""
    
    def __init__(self):
        super().__init__(SaleItem)
    
    def get_by_sale(self, db: Session, sale_id: int) -> List[SaleItem]:
        """Obtener items por venta"""
        return db.query(SaleItem).filter(
            and_(
                SaleItem.deleted_at.is_(None),
                SaleItem.sale_id == sale_id
            )
        ).all()
    
    def get_by_product(self, db: Session, product_id: int) -> List[SaleItem]:
        """Obtener items por producto"""
        return db.query(SaleItem).filter(
            and_(
                SaleItem.deleted_at.is_(None),
                SaleItem.product_id == product_id
            )
        ).all()

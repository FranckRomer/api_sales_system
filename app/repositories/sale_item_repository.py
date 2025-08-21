from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import SaleItem
from app.repositories.base import BaseRepository

class SaleItemRepository(BaseRepository[SaleItem]):
    """Repositorio para items de venta"""
    
    def __init__(self):
        super().__init__(SaleItem)
    
    def get_by_sale(self, db: Session, sale_id: int) -> List[SaleItem]:
        """Obtener todos los items de una venta específica"""
        return db.query(SaleItem).filter(
            and_(
                SaleItem.deleted_at.is_(None),
                SaleItem.sale_id == sale_id
            )
        ).all()
    
    def get_by_product(self, db: Session, product_id: int) -> List[SaleItem]:
        """Obtener todos los items de un producto específico"""
        return db.query(SaleItem).filter(
            and_(
                SaleItem.deleted_at.is_(None),
                SaleItem.product_id == product_id
            )
        ).all()

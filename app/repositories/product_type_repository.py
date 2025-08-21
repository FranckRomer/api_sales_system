from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import ProductType
from app.repositories.base import BaseRepository

class ProductTypeRepository(BaseRepository[ProductType]):
    """Repositorio para tipos de producto"""
    
    def __init__(self):
        super().__init__(ProductType)
    
    def get_by_name(self, db: Session, name: str) -> Optional[ProductType]:
        """Obtener tipo de producto por nombre"""
        return db.query(ProductType).filter(
            and_(
                ProductType.deleted_at.is_(None),
                ProductType.name == name
            )
        ).first()

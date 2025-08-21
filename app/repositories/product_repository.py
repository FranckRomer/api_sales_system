from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import Product, ProductType
from app.repositories.base import BaseRepository

class ProductRepository(BaseRepository[Product]):
    """Repositorio para operaciones con productos"""
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_name(self, db: Session, name: str) -> Optional[Product]:
        """Obtener producto por nombre"""
        return db.query(Product).filter(
            and_(
                Product.deleted_at.is_(None),
                Product.name == name
            )
        ).first()
    
    def get_by_type(self, db: Session, product_type_id: int) -> List[Product]:
        """Obtener productos por tipo"""
        return db.query(Product).filter(
            and_(
                Product.deleted_at.is_(None),
                Product.product_type_id == product_type_id
            )
        ).all()
    
    def get_with_relations(self, db: Session, product_id: int) -> Optional[Product]:
        """Obtener producto con sus relaciones (tipo)"""
        return db.query(Product).filter(
            and_(
                Product.deleted_at.is_(None),
                Product.product_id == product_id
            )
        ).first()

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

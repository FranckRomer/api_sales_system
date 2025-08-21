from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import CustomerType
from app.repositories.base import BaseRepository

class CustomerTypeRepository(BaseRepository[CustomerType]):
    """Repositorio para tipos de cliente"""
    
    def __init__(self):
        super().__init__(CustomerType)
    
    def get_by_name(self, db: Session, name: str) -> Optional[CustomerType]:
        """Obtener tipo de cliente por nombre"""
        return db.query(CustomerType).filter(
            and_(
                CustomerType.deleted_at.is_(None),
                CustomerType.name == name
            )
        ).first()

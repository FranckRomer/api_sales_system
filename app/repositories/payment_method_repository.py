from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import PaymentMethod
from app.repositories.base import BaseRepository

class PaymentMethodRepository(BaseRepository[PaymentMethod]):
    """Repositorio para métodos de pago"""
    
    def __init__(self):
        super().__init__(PaymentMethod)
    
    def get_by_name(self, db: Session, name: str) -> Optional[PaymentMethod]:
        """Obtener método de pago por nombre"""
        return db.query(PaymentMethod).filter(
            and_(
                PaymentMethod.deleted_at.is_(None),
                PaymentMethod.name == name
            )
        ).first()

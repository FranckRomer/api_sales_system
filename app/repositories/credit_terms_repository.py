from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import CreditTerms
from app.repositories.base import BaseRepository

class CreditTermsRepository(BaseRepository[CreditTerms]):
    """Repositorio para términos de crédito"""
    
    def __init__(self):
        super().__init__(CreditTerms)
    
    def get_by_days(self, db: Session, days: int) -> Optional[CreditTerms]:
        """Obtener términos de crédito por número de días"""
        return db.query(CreditTerms).filter(
            and_(
                CreditTerms.deleted_at.is_(None),
                CreditTerms.days == days
            )
        ).first()

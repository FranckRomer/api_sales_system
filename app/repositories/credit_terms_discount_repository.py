from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import CreditTermsDiscount
from app.repositories.base import BaseRepository

class CreditTermsDiscountRepository(BaseRepository[CreditTermsDiscount]):
    """Repositorio para descuentos por términos de crédito"""
    
    def __init__(self):
        super().__init__(CreditTermsDiscount)
    
    def get_by_credit_terms_id(self, db: Session, credit_terms_id: int) -> Optional[CreditTermsDiscount]:
        """Obtener descuento por ID de términos de crédito"""
        return db.query(CreditTermsDiscount).filter(
            and_(
                CreditTermsDiscount.deleted_at.is_(None),
                CreditTermsDiscount.credit_terms_id == credit_terms_id
            )
        ).first()
    
    def get_by_days(self, db: Session, days: int) -> Optional[CreditTermsDiscount]:
        """Obtener descuento por número de días de crédito"""
        from app.database.models import CreditTerms
        
        return db.query(CreditTermsDiscount).join(CreditTerms).filter(
            and_(
                CreditTermsDiscount.deleted_at.is_(None),
                CreditTerms.deleted_at.is_(None),
                CreditTerms.days == days
            )
        ).first()

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.models import Customer, CustomerType, CreditTerms
from app.repositories.base import BaseRepository

class CustomerRepository(BaseRepository[Customer]):
    """Repositorio para operaciones con clientes"""
    
    def __init__(self):
        super().__init__(Customer)
    
    def get_by_name(self, db: Session, name: str) -> Optional[Customer]:
        """Obtener cliente por nombre"""
        return db.query(Customer).filter(
            and_(
                Customer.deleted_at.is_(None),
                Customer.name == name
            )
        ).first()
    
    def get_by_type(self, db: Session, customer_type_id: int) -> List[Customer]:
        """Obtener clientes por tipo"""
        return db.query(Customer).filter(
            and_(
                Customer.deleted_at.is_(None),
                Customer.customer_type_id == customer_type_id
            )
        ).all()
    
    def get_with_relations(self, db: Session, customer_id: int) -> Optional[Customer]:
        """Obtener cliente con sus relaciones (tipo y términos de crédito)"""
        return db.query(Customer).filter(
            and_(
                Customer.deleted_at.is_(None),
                Customer.customer_id == customer_id
            )
        ).first()

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

class CreditTermsRepository(BaseRepository[CreditTerms]):
    """Repositorio para términos de crédito"""
    
    def __init__(self):
        super().__init__(CreditTerms)
    
    def get_by_days(self, db: Session, days: int) -> Optional[CreditTerms]:
        """Obtener términos de crédito por días"""
        return db.query(CreditTerms).filter(
            and_(
                CreditTerms.deleted_at.is_(None),
                CreditTerms.days == days
            )
        ).first()

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.connection import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Repositorio base con operaciones CRUD comunes
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Obtener un registro por ID"""
        # Buscar el campo de ID correcto (puede ser customer_id, product_id, etc.)
        id_field = self._get_id_field()
        filter_condition = and_(
            getattr(self.model, 'deleted_at').is_(None),
            getattr(self.model, id_field) == id
        )
        return db.query(self.model).filter(filter_condition).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtener todos los registros (sin soft-deleted)"""
        return db.query(self.model).filter(
            getattr(self.model, 'deleted_at').is_(None)
        ).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """Crear un nuevo registro"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Actualizar un registro existente"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def soft_delete(self, db: Session, id: Any) -> bool:
        """Soft delete de un registro"""
        from datetime import datetime
        db_obj = self.get(db, id)
        if db_obj:
            db_obj.deleted_at = datetime.now()
            db.commit()
            return True
        return False
    
    def hard_delete(self, db: Session, id: Any) -> bool:
        """Eliminación física de un registro"""
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
    
    def exists(self, db: Session, id: Any) -> bool:
        """Verificar si existe un registro"""
        id_field = self._get_id_field()
        filter_condition = and_(
            getattr(self.model, 'deleted_at').is_(None),
            getattr(self.model, id_field) == id
        )
        return db.query(self.model).filter(filter_condition).first() is not None
    
    def _get_id_field(self) -> str:
        """Obtener el nombre del campo de ID del modelo"""
        # Buscar el campo que termine en '_id' y sea primary key
        for column in self.model.__table__.columns:
            if column.name.endswith('_id') and column.primary_key:
                return column.name
        
        # Fallback: buscar cualquier campo que termine en '_id'
        for column in self.model.__table__.columns:
            if column.name.endswith('_id'):
                return column.name
        
        # Fallback final: usar 'id' si existe
        return 'id'

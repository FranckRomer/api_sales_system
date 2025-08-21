from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from app.config.settings import settings

# Crear el engine de SQLAlchemy
engine = create_engine(
    settings.database.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()

def get_db() -> Session:
    """
    Obtener una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """
    Eliminar todas las tablas (solo para desarrollo)
    """
    Base.metadata.drop_all(bind=engine)

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Customer, CustomerCreate
from app.database import db

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate):
    """
    Crear un nuevo cliente
    """
    try:
        return db.create_customer(customer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el cliente: {str(e)}"
        )

@router.get("/", response_model=List[Customer])
async def get_customers():
    """
    Obtener todos los clientes (oculta los soft-deleted)
    """
    try:
        return db.get_customers()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los clientes: {str(e)}"
        )

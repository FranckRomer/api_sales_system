from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Product, ProductCreate
from app.database import db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Crear un nuevo producto
    """
    try:
        return db.create_product(product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {str(e)}"
        )

@router.get("/", response_model=List[Product])
async def get_products():
    """
    Obtener todos los productos
    """
    try:
        return db.get_products()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los productos: {str(e)}"
        )

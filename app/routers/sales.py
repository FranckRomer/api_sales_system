from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Sale, SaleCreate, SaleList
from app.database import db

router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

@router.post("/", response_model=Sale, status_code=status.HTTP_201_CREATED)
async def create_sale(sale: SaleCreate):
    """
    Crear una nueva venta (endpoint core)
    """
    try:
        # Verificar que el cliente existe
        customer = db.get_customer(sale.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Verificar que los productos existen
        for item in sale.items:
            product = db.get_product(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {item.product_id} no encontrado"
                )
        
        return db.create_sale(sale)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la venta: {str(e)}"
        )

@router.get("/", response_model=List[SaleList])
async def get_sales():
    """
    Obtener todas las ventas (oculta las soft-deleted)
    """
    try:
        return db.get_sales()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las ventas: {str(e)}"
        )

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import Sale, SaleCreate, SaleList
from app.database.connection import get_db
from app.services.sale_service import SaleService
from app.repositories.sale_repository import SaleRepository

router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

@router.post("/", response_model=Sale, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale: SaleCreate, 
    db: Session = Depends(get_db)
):
    """
    Crear una nueva venta (endpoint core)
    """
    try:
        sale_service = SaleService()
        
        # Convertir el modelo Pydantic a diccionario para el servicio
        sale_data = {
            "customer_id": sale.customer_id,
            "payment_method_id": None,  # Necesitamos obtener el ID del método de pago
            "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in sale.items]
        }
        
        # Obtener el ID del método de pago por nombre
        from app.repositories.payment_method_repository import PaymentMethodRepository
        payment_method_repo = PaymentMethodRepository()
        payment_method = payment_method_repo.get_by_name(db, sale.payment_method)
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Método de pago '{sale.payment_method}' no encontrado"
            )
        
        sale_data["payment_method_id"] = payment_method.payment_method_id
        
        # Crear la venta usando el servicio
        db_sale = sale_service.create_sale(db, sale_data)
        
        # Obtener el breakdown completo
        sale_with_breakdown = sale_service.get_sale_with_breakdown(db, db_sale.sale_id)
        
        return Sale(**sale_with_breakdown)
        
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
async def get_sales(db: Session = Depends(get_db)):
    """
    Obtener todas las ventas (oculta las soft-deleted)
    """
    try:
        sale_repo = SaleRepository()
        db_sales = sale_repo.get_all(db)
        
        # Convertir a formato de respuesta de la API
        sales = []
        for db_sale in db_sales:
            sale = SaleList(
                sale_id=db_sale.sale_id,
                customer_id=db_sale.customer_id,
                payment_method=db_sale.payment_method.name,
                subtotal=db_sale.subtotal,
                tax=db_sale.tax,
                total=db_sale.total,
                total_discounts_amount=db_sale.total_discounts_amount,
                sale_datetime=db_sale.sale_datetime
            )
            sales.append(sale)
        
        return sales
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las ventas: {str(e)}"
        )

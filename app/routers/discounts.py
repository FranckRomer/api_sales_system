from fastapi import APIRouter, HTTPException, status
from app.models import ProductDiscount, ProductDiscountCreate, PaymentDiscount, PaymentDiscountCreate
from app.database import db

router = APIRouter(
    prefix="/discounts",
    tags=["discounts"]
)

@router.post("/product", response_model=ProductDiscount, status_code=status.HTTP_201_CREATED)
async def create_product_discount(discount: ProductDiscountCreate):
    """
    Crear un descuento para un tipo de producto específico
    """
    try:
        return db.create_product_discount(discount)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el descuento del producto: {str(e)}"
        )

@router.post("/payment", response_model=PaymentDiscount, status_code=status.HTTP_201_CREATED)
async def create_payment_discount(discount: PaymentDiscountCreate):
    """
    Crear un descuento por método de pago
    """
    try:
        return db.create_payment_discount(discount)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el descuento de pago: {str(e)}"
        )

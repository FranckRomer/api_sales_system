from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models import ProductDiscount, ProductDiscountCreate, PaymentDiscount, PaymentDiscountCreate
from app.database.connection import get_db
from app.repositories.discount_repository import ProductTypeDiscountRepository, PaymentMethodDiscountRepository
from app.repositories.product_type_repository import ProductTypeRepository
from app.repositories.payment_method_repository import PaymentMethodRepository

router = APIRouter(
    prefix="/discounts",
    tags=["discounts"]
)

@router.post("/product", response_model=ProductDiscount, status_code=status.HTTP_201_CREATED)
async def create_product_discount(
    discount: ProductDiscountCreate, 
    db: Session = Depends(get_db)
):
    """
    Crear un descuento para un tipo de producto específico
    """
    try:
        # Verificar que el tipo de producto existe
        product_type_repo = ProductTypeRepository()
        product_type = product_type_repo.get_by_name(db, discount.product_type)
        if not product_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de producto '{discount.product_type}' no encontrado"
            )
        
        # Crear el descuento
        discount_repo = ProductTypeDiscountRepository()
        discount_data = {
            "product_type_id": product_type.product_type_id,
            "discount_percent": discount.discount_percent
        }
        
        db_discount = discount_repo.create(db, discount_data)
        
        # Retornar en el formato esperado por la API
        return ProductDiscount(
            product_type=product_type.name,
            discount_percent=db_discount.discount_percent
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el descuento del producto: {str(e)}"
        )

@router.post("/payment", response_model=PaymentDiscount, status_code=status.HTTP_201_CREATED)
async def create_payment_discount(
    discount: PaymentDiscountCreate, 
    db: Session = Depends(get_db)
):
    """
    Crear un descuento por método de pago
    """
    try:
        # Verificar que el método de pago existe
        payment_method_repo = PaymentMethodRepository()
        payment_method = payment_method_repo.get_by_name(db, discount.payment_method)
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Método de pago '{discount.payment_method}' no encontrado"
            )
        
        # Crear el descuento
        discount_repo = PaymentMethodDiscountRepository()
        discount_data = {
            "payment_method_id": payment_method.payment_method_id,
            "discount_percent": discount.discount_percent
        }
        
        db_discount = discount_repo.create(db, discount_data)
        
        # Retornar en el formato esperado por la API
        return PaymentDiscount(
            payment_method=payment_method.name,
            discount_percent=db_discount.discount_percent
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el descuento de pago: {str(e)}"
        )

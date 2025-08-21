from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import Product, ProductCreate
from app.database.connection import get_db
from app.repositories.product_repository import ProductRepository
from app.repositories.product_type_repository import ProductTypeRepository

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo producto
    """
    try:
        product_repo = ProductRepository()
        
        # Verificar que el tipo de producto existe
        product_type_repo = ProductTypeRepository()
        product_type = product_type_repo.get_by_name(db, product.product_type)
        if not product_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de producto '{product.product_type}' no válido"
            )
        
        # Crear el producto
        product_data = {
            "name": product.name,
            "product_type_id": product_type.product_type_id,
            "list_price": product.list_price
        }
        
        db_product = product_repo.create(db, product_data)
        
        # Retornar en el formato esperado por la API
        return Product(
            product_id=db_product.product_id,
            name=db_product.name,
            product_type=product_type.name,
            list_price=db_product.list_price
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {str(e)}"
        )

@router.get("/", response_model=List[Product])
async def get_products(db: Session = Depends(get_db)):
    """
    Obtener todos los productos
    """
    try:
        product_repo = ProductRepository()
        db_products = product_repo.get_all(db)
        
        # Convertir a formato de respuesta de la API
        products = []
        for db_product in db_products:
            product = Product(
                product_id=db_product.product_id,
                name=db_product.name,
                product_type=db_product.product_type_ref.name,
                list_price=db_product.list_price
            )
            products.append(product)
        
        return products
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los productos: {str(e)}"
        )

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import Customer, CustomerCreate
from app.database.connection import get_db
from app.repositories.customer_repository import CustomerRepository
from app.repositories.customer_type_repository import CustomerTypeRepository
from app.repositories.credit_terms_repository import CreditTermsRepository

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer: CustomerCreate, 
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo cliente
    """
    try:
        customer_repo = CustomerRepository()
        
        # Verificar que el tipo de cliente existe
        customer_type_repo = CustomerTypeRepository()
        customer_type = customer_type_repo.get_by_name(db, customer.customer_type)
        if not customer_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de cliente '{customer.customer_type}' no válido. Tipos válidos: VIP, Regular"
            )
        
        # Verificar que los términos de crédito existen
        credit_terms_repo = CreditTermsRepository()
        credit_terms = credit_terms_repo.get_by_days(db, customer.credit_terms_days)
        if not credit_terms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Términos de crédito de {customer.credit_terms_days} días no válidos"
            )
        
        # Crear el cliente
        customer_data = {
            "name": customer.name,
            "customer_type_id": customer_type.customer_type_id,
            "credit_terms_id": credit_terms.credit_terms_id
        }
        
        db_customer = customer_repo.create(db, customer_data)
        
        # Retornar en el formato esperado por la API
        return Customer(
            customer_id=db_customer.customer_id,
            name=db_customer.name,
            customer_type=customer_type.name,
            credit_terms_days=credit_terms.days
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el cliente: {str(e)}"
        )

@router.get("/", response_model=List[Customer])
async def get_customers(db: Session = Depends(get_db)):
    """
    Obtener todos los clientes (oculta los soft-deleted)
    """
    try:
        customer_repo = CustomerRepository()
        db_customers = customer_repo.get_all(db)
        
        # Convertir a formato de respuesta de la API
        customers = []
        for db_customer in db_customers:
            customer = Customer(
                customer_id=db_customer.customer_id,
                name=db_customer.name,
                customer_type=db_customer.customer_type_ref.name,
                credit_terms_days=db_customer.credit_terms_ref.days
            )
            customers.append(customer)
        
        return customers
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los clientes: {str(e)}"
        )

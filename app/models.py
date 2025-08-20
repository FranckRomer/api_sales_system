from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Customer Models
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    customer_type: str = Field(..., pattern="^(VIP|Regular)$")
    credit_terms_days: int = Field(..., ge=0, le=365)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int
    name: str
    customer_type: str
    credit_terms_days: int

# Product Models
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    product_type: str = Field(..., min_length=1, max_length=50)
    list_price: Decimal = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    name: str
    product_type: str
    list_price: Decimal

# Discount Models
class ProductDiscountCreate(BaseModel):
    product_type: str = Field(..., min_length=1, max_length=50)
    discount_percent: Decimal = Field(..., ge=0, le=100)

class ProductDiscount(ProductDiscountCreate):
    pass

class PaymentDiscountCreate(BaseModel):
    payment_method: str = Field(..., min_length=1, max_length=50)
    discount_percent: Decimal = Field(..., ge=0, le=100)

class PaymentDiscount(PaymentDiscountCreate):
    pass

# Sale Models
class SaleItem(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)

class SaleCreate(BaseModel):
    customer_id: int
    payment_method: str = Field(..., min_length=1, max_length=50)
    items: List[SaleItem] = Field(..., min_length=1)

class SaleItemBreakdown(BaseModel):
    product_id: int
    quantity: int
    list_price: Decimal
    discounts: dict = Field(..., description="Diccionario con descuentos aplicados")
    line_subtotal_after_discounts: Decimal

class SaleBreakdown(BaseModel):
    lines: List[SaleItemBreakdown]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    total_discounts_amount: Decimal

class Sale(BaseModel):
    sale_id: int
    customer_id: int
    payment_method: str
    tax_rate_percent: Decimal = Field(default=16.0)
    breakdown: SaleBreakdown

class SaleList(BaseModel):
    sale_id: int
    customer_id: int
    payment_method: str
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    total_discounts_amount: Decimal
    sale_datetime: datetime

# Configuración global para todos los modelos
for model in [CustomerBase, ProductBase, ProductDiscountCreate, PaymentDiscountCreate, SaleItem, SaleCreate, SaleItemBreakdown, SaleBreakdown, Sale, SaleList]:
    model.model_config = ConfigDict(
        json_encoders={Decimal: str},
        arbitrary_types_allowed=True
    )

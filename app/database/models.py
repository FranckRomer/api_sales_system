from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class CustomerType(Base):
    """Modelo para tipos de cliente"""
    __tablename__ = "customer_type"
    
    customer_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    customers = relationship("Customer", back_populates="customer_type_ref")
    
    __table_args__ = (
        Index('idx_customer_type_deleted', 'deleted_at'),
    )

class CreditTerms(Base):
    """Modelo para términos de crédito"""
    __tablename__ = "credit_terms"
    
    credit_terms_id = Column(Integer, primary_key=True, autoincrement=True)
    days = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    customers = relationship("Customer", back_populates="credit_terms_ref")
    credit_terms_discounts = relationship("CreditTermsDiscount", back_populates="credit_terms")

class Customer(Base):
    """Modelo para clientes"""
    __tablename__ = "customer"
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    customer_type_id = Column(Integer, ForeignKey("customer_type.customer_type_id"), nullable=False)
    credit_terms_id = Column(Integer, ForeignKey("credit_terms.credit_terms_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    customer_type_ref = relationship("CustomerType", back_populates="customers")
    credit_terms_ref = relationship("CreditTerms", back_populates="customers")
    sales = relationship("Sale", back_populates="customer")
    
    __table_args__ = (
        Index('idx_customer_deleted', 'deleted_at'),
    )

class ProductType(Base):
    """Modelo para tipos de producto"""
    __tablename__ = "product_type"
    
    product_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    products = relationship("Product", back_populates="product_type_ref")
    product_type_discounts = relationship("ProductTypeDiscount", back_populates="product_type")

class Product(Base):
    """Modelo para productos"""
    __tablename__ = "product"
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    product_type_id = Column(Integer, ForeignKey("product_type.product_type_id"), nullable=False)
    list_price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    product_type_ref = relationship("ProductType", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")
    
    __table_args__ = (
        CheckConstraint("list_price >= 0", name="check_list_price_positive"),
        Index('idx_product_deleted', 'deleted_at'),
    )

class PaymentMethod(Base):
    """Modelo para métodos de pago"""
    __tablename__ = "payment_method"
    
    payment_method_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    sales = relationship("Sale", back_populates="payment_method")
    payment_method_discounts = relationship("PaymentMethodDiscount", back_populates="payment_method")

class ProductTypeDiscount(Base):
    """Modelo para descuentos por tipo de producto"""
    __tablename__ = "product_type_discount"
    
    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    product_type_id = Column(Integer, ForeignKey("product_type.product_type_id"), nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    product_type = relationship("ProductType", back_populates="product_type_discounts")
    
    __table_args__ = (
        CheckConstraint("discount_percent >= 0 AND discount_percent <= 100", name="check_discount_percent_range"),
    )

class PaymentMethodDiscount(Base):
    """Modelo para descuentos por método de pago"""
    __tablename__ = "payment_method_discount"
    
    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    payment_method_id = Column(Integer, ForeignKey("payment_method.payment_method_id"), nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    payment_method = relationship("PaymentMethod", back_populates="payment_method_discounts")
    
    __table_args__ = (
        CheckConstraint("discount_percent >= 0 AND discount_percent <= 100", name="check_discount_percent_range"),
    )

class CreditTermsDiscount(Base):
    """Modelo para descuentos por términos de crédito"""
    __tablename__ = "credit_terms_discount"
    
    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    credit_terms_id = Column(Integer, ForeignKey("credit_terms.credit_terms_id"), nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    credit_terms = relationship("CreditTerms", back_populates="credit_terms_discounts")
    
    __table_args__ = (
        CheckConstraint("discount_percent >= 0 AND discount_percent <= 100", name="check_credit_terms_discount_percent_range"),
        Index('idx_credit_terms_discount_terms', 'credit_terms_id'),
    )

class Sale(Base):
    """Modelo para ventas"""
    __tablename__ = "sale"
    
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_method.payment_method_id"), nullable=False)
    tax_rate_percent = Column(DECIMAL(5, 2), nullable=False, server_default="16.0")
    subtotal = Column(DECIMAL(12, 2), nullable=False)
    tax = Column(DECIMAL(12, 2), nullable=False)
    total = Column(DECIMAL(12, 2), nullable=False)
    total_discounts_amount = Column(DECIMAL(12, 2), nullable=False, server_default="0")
    sale_datetime = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    customer = relationship("Customer", back_populates="sales")
    payment_method = relationship("PaymentMethod", back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale")
    
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="check_subtotal_positive"),
        CheckConstraint("tax >= 0", name="check_tax_positive"),
        CheckConstraint("total >= 0", name="check_total_positive"),
        CheckConstraint("total_discounts_amount >= 0", name="check_total_discounts_positive"),
        Index('idx_sale_deleted', 'deleted_at'),
        Index('idx_sale_customer', 'customer_id'),
        Index('idx_sale_datetime', 'sale_datetime'),
    )

class SaleItem(Base):
    """Modelo para items de venta"""
    __tablename__ = "sale_item"
    
    sale_item_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey("sale.sale_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    list_price = Column(DECIMAL(10, 2), nullable=False)
    product_type_discount = Column(DECIMAL(10, 2), nullable=False, server_default="0")
    payment_method_discount = Column(DECIMAL(10, 2), nullable=False, server_default="0")
    credit_terms_discount = Column(DECIMAL(10, 2), nullable=False, server_default="0")
    line_subtotal_after_discounts = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime)
    
    # Relaciones
    sale = relationship("Sale", back_populates="sale_items")
    product = relationship("Product", back_populates="sale_items")
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("list_price >= 0", name="check_list_price_positive"),
        CheckConstraint("product_type_discount >= 0", name="check_product_type_discount_positive"),
        CheckConstraint("payment_method_discount >= 0", name="check_payment_method_discount_positive"),
        CheckConstraint("credit_terms_discount >= 0", name="check_credit_terms_discount_positive"),
        CheckConstraint("line_subtotal_after_discounts >= 0", name="check_line_subtotal_positive"),
        Index('idx_sale_item_sale', 'sale_id'),
        Index('idx_sale_item_product', 'product_id'),
    )

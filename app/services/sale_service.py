from typing import Dict, List, Any
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from app.database.models import Sale, SaleItem, Customer, Product, PaymentMethod
from app.repositories.sale_repository import SaleRepository
from app.repositories.sale_item_repository import SaleItemRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.discount_repository import ProductTypeDiscountRepository, PaymentMethodDiscountRepository
from app.repositories.credit_terms_discount_repository import CreditTermsDiscountRepository

class SaleService:
    """Servicio para la lógica de negocio de ventas"""
    
    def __init__(self):
        self.sale_repo = SaleRepository()
        self.sale_item_repo = SaleItemRepository()
        self.customer_repo = CustomerRepository()
        self.product_repo = ProductRepository()
        self.payment_method_repo = PaymentMethodRepository()
        self.product_type_discount_repo = ProductTypeDiscountRepository()
        self.payment_method_discount_repo = PaymentMethodDiscountRepository()
        self.credit_terms_discount_repo = CreditTermsDiscountRepository()
    
    def create_sale(self, db: Session, sale_data: Dict[str, Any]) -> Sale:
        """
        Crear una venta con la nueva lógica de descuentos secuenciales
        
        Reglas de negocio:
        - Descuentos secuenciales: Base → ProductType → PaymentMethod → CreditTerms
        - Redondear cada línea a 2 decimales
        - Solo aplicar descuento de crédito si payment_method = "Store Credit"
        - Tax 16% sobre subtotal después de descuentos
        """
        # Validar que el cliente existe
        customer = self.customer_repo.get(db, sale_data["customer_id"])
        if not customer:
            raise ValueError("Cliente no encontrado")
        
        # Validar que el método de pago existe
        payment_method = self.payment_method_repo.get(db, sale_data["payment_method_id"])
        if not payment_method:
            raise ValueError("Método de pago no encontrado")
        
        # Validar productos y calcular descuentos
        items_data = []
        subtotal = Decimal('0')
        total_discounts = Decimal('0')
        
        for item in sale_data["items"]:
            product = self.product_repo.get(db, item["product_id"])
            if not product:
                raise ValueError(f"Producto con ID {item['product_id']} no encontrado")
            
            if item["quantity"] <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            
            # Calcular descuentos secuenciales
            line_total = self._calculate_line_discounts(
                db, product, payment_method, customer, item["quantity"]
            )
            
            items_data.append({
                "product": product,
                "quantity": item["quantity"],
                "line_total": line_total["line_total"],
                "discounts": line_total["discounts"]
            })
            
            subtotal += line_total["line_total"]
            total_discounts += line_total["discounts"]["total_discount"]
        
        # Calcular impuestos (16%)
        tax_rate = Decimal('16.0')
        tax = (subtotal * tax_rate / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Calcular total
        total = subtotal + tax
        
        # Crear la venta
        sale_data_db = {
            "customer_id": customer.customer_id,
            "payment_method_id": payment_method.payment_method_id,
            "tax_rate_percent": tax_rate,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "total_discounts_amount": total_discounts
        }
        
        db_sale = self.sale_repo.create(db, sale_data_db)
        
        # Crear los items de venta
        for item_data in items_data:
            sale_item_data = {
                "sale_id": db_sale.sale_id,
                "product_id": item_data["product"].product_id,
                "quantity": item_data["quantity"],
                "list_price": item_data["product"].list_price,
                "product_type_discount": item_data["discounts"]["product_type_discount"],
                "payment_method_discount": item_data["discounts"]["payment_method_discount"],
                "credit_terms_discount": item_data["discounts"]["credit_terms_discount"],
                "line_subtotal_after_discounts": item_data["line_total"]
            }
            
            self.sale_item_repo.create(db, sale_item_data)
        
        return db_sale
    
    def _calculate_line_discounts(
        self, 
        db: Session, 
        product: Product, 
        payment_method: PaymentMethod, 
        customer: Customer, 
        quantity: int
    ) -> Dict[str, Any]:
        """
        Calcular descuentos secuenciales para una línea de producto
        
        Secuencia: Base → ProductType → PaymentMethod → CreditTerms
        """
        # Precio base de la línea
        line_base = product.list_price * quantity
        
        # 1. Descuento por tipo de producto
        product_type_discount = self._get_product_type_discount(db, product.product_type_id)
        line_after_product_discount = line_base * (1 - product_type_discount / Decimal('100'))
        line_after_product_discount = line_after_product_discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # 2. Descuento por método de pago
        payment_method_discount = self._get_payment_method_discount(db, payment_method.payment_method_id)
        line_after_payment_discount = line_after_product_discount * (1 - payment_method_discount / Decimal('100'))
        line_after_payment_discount = line_after_payment_discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # 3. Descuento por términos de crédito (solo si es Store Credit)
        credit_terms_discount = Decimal('0')
        if payment_method.name == "Store Credit":
            credit_terms_discount = self._get_credit_terms_discount(db, customer.credit_terms_id)
            line_after_credit_discount = line_after_payment_discount * (1 - credit_terms_discount / Decimal('100'))
            line_after_credit_discount = line_after_credit_discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            line_after_credit_discount = line_after_payment_discount
        
        # Calcular montos de descuento
        product_type_discount_amount = (line_base - line_after_product_discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        payment_method_discount_amount = (line_after_product_discount - line_after_payment_discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        credit_terms_discount_amount = (line_after_payment_discount - line_after_credit_discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        total_discount = product_type_discount_amount + payment_method_discount_amount + credit_terms_discount_amount
        
        return {
            "line_total": line_after_credit_discount,
            "discounts": {
                "product_type_discount": product_type_discount_amount,
                "payment_method_discount": payment_method_discount_amount,
                "credit_terms_discount": credit_terms_discount_amount,
                "total_discount": total_discount
            }
        }
    
    def _get_product_type_discount(self, db: Session, product_type_id: int) -> Decimal:
        """Obtener descuento por tipo de producto"""
        discount = self.product_type_discount_repo.get_by_product_type(db, product_type_id)
        return Decimal(discount.discount_percent) if discount else Decimal('0')
    
    def _get_payment_method_discount(self, db: Session, payment_method_id: int) -> Decimal:
        """Obtener descuento por método de pago"""
        discount = self.payment_method_discount_repo.get_by_payment_method(db, payment_method_id)
        return Decimal(discount.discount_percent) if discount else Decimal('0')
    
    def _get_credit_terms_discount(self, db: Session, credit_terms_id: int) -> Decimal:
        """Obtener descuento por términos de crédito"""
        discount = self.credit_terms_discount_repo.get_by_credit_terms_id(db, credit_terms_id)
        return Decimal(discount.discount_percent) if discount else Decimal('0')
    
    def get_sale_with_breakdown(self, db: Session, sale_id: int) -> Dict[str, Any]:
        """Obtener venta con breakdown detallado para la respuesta de la API"""
        sale = self.sale_repo.get(db, sale_id)
        if not sale:
            raise ValueError("Venta no encontrada")
        
        # Obtener items de la venta
        sale_items = self.sale_item_repo.get_by_sale(db, sale_id)
        
        # Construir breakdown
        lines = []
        for item in sale_items:
            product = self.product_repo.get(db, item.product_id)
            lines.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "list_price": str(item.list_price),
                "discounts": {
                    "product_type": str(item.product_type_discount),
                    "payment_method": str(item.payment_method_discount),
                    "credit_terms": str(item.credit_terms_discount)
                },
                "line_subtotal_after_discounts": str(item.line_subtotal_after_discounts)
            })
        
        # Obtener nombres para la respuesta
        customer = self.customer_repo.get(db, sale.customer_id)
        payment_method = self.payment_method_repo.get(db, sale.payment_method_id)
        
        return {
            "sale_id": sale.sale_id,
            "customer_id": sale.customer_id,
            "payment_method": payment_method.name,
            "tax_rate_percent": str(sale.tax_rate_percent),
            "breakdown": {
                "lines": lines,
                "subtotal": str(sale.subtotal),
                "tax": str(sale.tax),
                "total": str(sale.total),
                "total_discounts_amount": str(sale.total_discounts_amount)
            }
        }

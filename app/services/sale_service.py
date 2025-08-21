from decimal import Decimal
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database.models import Sale, SaleItem, Product, Customer, PaymentMethod
from app.repositories.sale_repository import SaleRepository, SaleItemRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.discount_repository import ProductTypeDiscountRepository, PaymentMethodDiscountRepository

class SaleService:
    """Servicio para la lógica de negocio de ventas"""
    
    def __init__(self):
        self.sale_repo = SaleRepository()
        self.sale_item_repo = SaleItemRepository()
        self.product_repo = ProductRepository()
        self.customer_repo = CustomerRepository()
        self.product_discount_repo = ProductTypeDiscountRepository()
        self.payment_discount_repo = PaymentMethodDiscountRepository()
    
    def create_sale(self, db: Session, sale_data: Dict[str, Any]) -> Sale:
        """Crear una venta completa con cálculo de descuentos e impuestos"""
        
        # Validar que el cliente existe
        customer = self.customer_repo.get(db, sale_data["customer_id"])
        if not customer:
            raise ValueError("Cliente no encontrado")
        
        # Validar que el método de pago existe
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.payment_method_id == sale_data["payment_method_id"]
        ).first()
        if not payment_method:
            raise ValueError("Método de pago no encontrado")
        
        # Calcular totales y descuentos
        subtotal = Decimal('0')
        total_discounts = Decimal('0')
        sale_items = []
        
        for item_data in sale_data["items"]:
            # Obtener producto
            product = self.product_repo.get(db, item_data["product_id"])
            if not product:
                raise ValueError(f"Producto con ID {item_data['product_id']} no encontrado")
            
            quantity = item_data["quantity"]
            list_price = product.list_price
            
            # Calcular descuentos
            product_type_discount = self._calculate_product_type_discount(db, product, list_price, quantity)
            payment_method_discount = self._calculate_payment_method_discount(db, payment_method, list_price, quantity)
            credit_terms_discount = self._calculate_credit_terms_discount(customer, list_price, quantity)
            
            # Calcular subtotal de la línea
            line_total = list_price * quantity
            line_discounts = product_type_discount + payment_method_discount + credit_terms_discount
            line_subtotal = line_total - line_discounts
            
            # Acumular totales
            subtotal += line_subtotal
            total_discounts += line_discounts
            
            # Crear item de venta
            sale_item = SaleItem(
                sale_id=None,  # Se asignará después
                product_id=product.product_id,
                quantity=quantity,
                list_price=list_price,
                product_type_discount=product_type_discount,
                payment_method_discount=payment_method_discount,
                credit_terms_discount=credit_terms_discount,
                line_subtotal_after_discounts=line_subtotal
            )
            sale_items.append(sale_item)
        
        # Calcular impuestos (16% por defecto)
        tax_rate = Decimal('16.0')
        tax = subtotal * tax_rate / 100
        total = subtotal + tax
        
        # Crear la venta
        sale = Sale(
            customer_id=customer.customer_id,
            payment_method_id=payment_method.payment_method_id,
            tax_rate_percent=tax_rate,
            subtotal=subtotal,
            tax=tax,
            total=total,
            total_discounts_amount=total_discounts
        )
        
        # Guardar la venta
        db.add(sale)
        db.flush()  # Para obtener el ID de la venta
        
        # Asignar el ID de la venta a los items y guardarlos
        for item in sale_items:
            item.sale_id = sale.sale_id
            db.add(item)
        
        db.commit()
        db.refresh(sale)
        
        return sale
    
    def _calculate_product_type_discount(self, db: Session, product: Product, list_price: Decimal, quantity: int) -> Decimal:
        """Calcular descuento por tipo de producto"""
        discount = self.product_discount_repo.get_by_product_type(db, product.product_type_id)
        if discount:
            return (list_price * quantity * discount.discount_percent) / 100
        return Decimal('0')
    
    def _calculate_payment_method_discount(self, db: Session, payment_method: PaymentMethod, list_price: Decimal, quantity: int) -> Decimal:
        """Calcular descuento por método de pago"""
        discount = self.payment_discount_repo.get_by_payment_method(db, payment_method.payment_method_id)
        if discount:
            return (list_price * quantity * discount.discount_percent) / 100
        return Decimal('0')
    
    def _calculate_credit_terms_discount(self, customer: Customer, list_price: Decimal, quantity: int) -> Decimal:
        """Calcular descuento por términos de crédito (solo para Store Credit)"""
        # Verificar si es Store Credit (esto dependerá de tu lógica de negocio)
        # Por ahora, aplicamos un descuento fijo del 1.9% para Store Credit
        if hasattr(customer, 'payment_method') and customer.payment_method == "Store Credit":
            return (list_price * quantity * Decimal('1.9')) / 100
        return Decimal('0')
    
    def get_sale_with_breakdown(self, db: Session, sale_id: int) -> Dict[str, Any]:
        """Obtener venta con breakdown detallado"""
        sale = self.sale_repo.get_with_items(db, sale_id)
        if not sale:
            raise ValueError("Venta no encontrada")
        
        # Construir breakdown
        lines = []
        for item in sale.sale_items:
            line = {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "list_price": item.list_price,
                "discounts": {
                    "product_type": item.product_type_discount,
                    "payment_method": item.payment_method_discount,
                    "credit_terms": item.credit_terms_discount
                },
                "line_subtotal_after_discounts": item.line_subtotal_after_discounts
            }
            lines.append(line)
        
        breakdown = {
            "lines": lines,
            "subtotal": sale.subtotal,
            "tax": sale.tax,
            "total": sale.total,
            "total_discounts_amount": sale.total_discounts_amount
        }
        
        return {
            "sale_id": sale.sale_id,
            "customer_id": sale.customer_id,
            "payment_method": sale.payment_method.name,
            "tax_rate_percent": sale.tax_rate_percent,
            "breakdown": breakdown
        }

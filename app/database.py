from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional
from app.models import (
    Customer, CustomerCreate, 
    Product, ProductCreate, 
    ProductDiscount, ProductDiscountCreate,
    PaymentDiscount, PaymentDiscountCreate,
    Sale, SaleCreate, SaleList
)

# Base de datos simulada en memoria
class Database:
    def __init__(self):
        self.customers: Dict[int, Customer] = {}
        self.products: Dict[int, Product] = {}
        self.product_discounts: Dict[str, ProductDiscount] = {}
        self.payment_discounts: Dict[str, PaymentDiscount] = {}
        self.sales: Dict[int, SaleList] = {}
        self._customer_id_counter = 1
        self._product_id_counter = 1
        self._sale_id_counter = 1001

    # Customer methods
    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        customer = Customer(
            customer_id=self._customer_id_counter,
            name=customer_data.name,
            customer_type=customer_data.customer_type,
            credit_terms_days=customer_data.credit_terms_days
        )
        self.customers[customer.customer_id] = customer
        self._customer_id_counter += 1
        return customer

    def get_customers(self) -> List[Customer]:
        return list(self.customers.values())

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.customers.get(customer_id)

    # Product methods
    def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(
            product_id=self._product_id_counter,
            name=product_data.name,
            product_type=product_data.product_type,
            list_price=product_data.list_price
        )
        self.products[product.product_id] = product
        self._product_id_counter += 1
        return product

    def get_products(self) -> List[Product]:
        return list(self.products.values())

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)

    # Discount methods
    def create_product_discount(self, discount_data: ProductDiscountCreate) -> ProductDiscount:
        discount = ProductDiscount(
            product_type=discount_data.product_type,
            discount_percent=discount_data.discount_percent
        )
        self.product_discounts[discount.product_type] = discount
        return discount

    def create_payment_discount(self, discount_data: PaymentDiscountCreate) -> PaymentDiscount:
        discount = PaymentDiscount(
            payment_method=discount_data.payment_method,
            discount_percent=discount_data.discount_percent
        )
        self.payment_discounts[discount.payment_method] = discount
        return discount

    def get_product_discount(self, product_type: str) -> Optional[ProductDiscount]:
        return self.product_discounts.get(product_type)

    def get_payment_discount(self, payment_method: str) -> Optional[PaymentDiscount]:
        return self.payment_discounts.get(payment_method)

    # Sale methods
    def create_sale(self, sale_data: SaleCreate) -> Sale:
        # Obtener información del cliente
        customer = self.get_customer(sale_data.customer_id)
        if not customer:
            raise ValueError("Cliente no encontrado")

        # Calcular descuentos y totales
        lines = []
        subtotal = Decimal('0')
        total_discounts = Decimal('0')

        for item in sale_data.items:
            product = self.get_product(item.product_id)
            if not product:
                raise ValueError(f"Producto con ID {item.product_id} no encontrado")

            # Calcular descuentos por tipo de producto
            product_discount = self.get_product_discount(product.product_type)
            product_discount_amount = Decimal('0')
            if product_discount:
                product_discount_amount = (product.list_price * item.quantity * product_discount.discount_percent) / 100

            # Calcular descuentos por método de pago
            payment_discount = self.get_payment_discount(sale_data.payment_method)
            payment_discount_amount = Decimal('0')
            if payment_discount:
                payment_discount_amount = (product.list_price * item.quantity * payment_discount.discount_percent) / 100

            # Calcular descuentos por términos de crédito (solo para Store Credit)
            credit_terms_discount_amount = Decimal('0')
            if sale_data.payment_method == "Store Credit":
                credit_terms_discount_amount = (product.list_price * item.quantity * Decimal('1.9')) / 100

            # Calcular subtotal de la línea después de descuentos
            line_total = product.list_price * item.quantity
            line_discounts = product_discount_amount + payment_discount_amount + credit_terms_discount_amount
            line_subtotal_after_discounts = line_total - line_discounts

            # Crear breakdown de la línea
            line_breakdown = {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "list_price": product.list_price,
                "discounts": {
                    "product_type": product_discount_amount,
                    "payment_method": payment_discount_amount,
                    "credit_terms": credit_terms_discount_amount
                },
                "line_subtotal_after_discounts": line_subtotal_after_discounts
            }
            lines.append(line_breakdown)

            subtotal += line_subtotal_after_discounts
            total_discounts += line_discounts

        # Calcular impuestos (16% por defecto)
        tax_rate = Decimal('16.0')
        tax = subtotal * tax_rate / 100
        total = subtotal + tax

        # Crear breakdown de la venta
        breakdown = {
            "lines": lines,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "total_discounts_amount": total_discounts
        }

        # Crear la venta
        sale = Sale(
            sale_id=self._sale_id_counter,
            customer_id=sale_data.customer_id,
            payment_method=sale_data.payment_method,
            tax_rate_percent=tax_rate,
            breakdown=breakdown
        )

        # Crear registro de venta para el listado
        sale_list = SaleList(
            sale_id=sale.sale_id,
            customer_id=sale.customer_id,
            payment_method=sale.payment_method,
            subtotal=sale.breakdown.subtotal,
            tax=sale.breakdown.tax,
            total=sale.breakdown.total,
            total_discounts_amount=sale.breakdown.total_discounts_amount,
            sale_datetime=datetime.now()
        )

        self.sales[sale.sale_id] = sale_list
        self._sale_id_counter += 1

        return sale

    def get_sales(self) -> List[SaleList]:
        return list(self.sales.values())

    def get_sale(self, sale_id: int) -> Optional[SaleList]:
        return self.sales.get(sale_id)

# Instancia global de la base de datos
db = Database()

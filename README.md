# API Sales System

Sistema de API para gestión de ventas desarrollado con FastAPI.

## 🚀 Características

- API RESTful con FastAPI
- Documentación automática con Swagger/OpenAPI
- Tipado estático con Python
- Gestión completa de clientes, productos, descuentos y ventas
- Validación de datos con Pydantic
- Base de datos en memoria para desarrollo
- Tests automatizados con pytest
- Cálculo automático de descuentos e impuestos

## 📋 Requisitos

- Python 3.8+
- pip

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/api_sales_system.git
cd api_sales_system
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. Activa el entorno virtual:
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Ejecuta la aplicación:
```bash
uvicorn main:app --reload
```

3. Abre tu navegador y ve a:
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs
   - Documentación alternativa: http://localhost:8000/redoc

## 📚 Endpoints Disponibles

### 👥 Clientes
- `POST /customers` - Crear un nuevo cliente
- `GET /customers` - Obtener todos los clientes

### 📦 Productos
- `POST /products` - Crear un nuevo producto
- `GET /products` - Obtener todos los productos

### 🎯 Descuentos
- `POST /discounts/product` - Crear descuento por tipo de producto
- `POST /discounts/payment` - Crear descuento por método de pago

### 💰 Ventas
- `POST /sales` - Crear una nueva venta (endpoint core)
- `GET /sales` - Obtener todas las ventas

### 🔍 Otros
- `GET /` - Información de la API
- `GET /health` - Estado de salud de la API

## 🧪 Pruebas

Para ejecutar las pruebas:
```bash
pytest
```

Para ejecutar con más detalle:
```bash
pytest -v
```

## 📝 Estructura del Proyecto

```
api_sales_system/
├── app/
│   ├── __init__.py
│   ├── models.py          # Modelos Pydantic
│   ├── database.py        # Base de datos simulada
│   └── routers/           # Endpoints organizados
│       ├── __init__.py
│       ├── customers.py   # Endpoints de clientes
│       ├── products.py    # Endpoints de productos
│       ├── discounts.py   # Endpoints de descuentos
│       └── sales.py       # Endpoints de ventas
├── tests/                 # Tests automatizados
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_products.py
│   ├── test_discounts.py
│   └── test_sales.py
├── main.py                # Aplicación principal
├── requirements.txt       # Dependencias
├── pytest.ini            # Configuración de pytest
├── README.md             # Este archivo
├── LICENSE               # Licencia MIT
└── .gitignore            # Archivos a ignorar en Git
```

## 🔧 Desarrollo

### Formateo de código
```bash
black .
```

### Linting
```bash
flake8 .
```

### Instalar dependencias de desarrollo
```bash
pip install -r requirements.txt
```

## 📊 Ejemplos de Uso

### Crear un Cliente
```bash
curl -X POST "http://localhost:8000/customers/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Ana",
       "customer_type": "VIP",
       "credit_terms_days": 90
     }'
```

### Crear un Producto
```bash
curl -X POST "http://localhost:8000/products/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop",
       "product_type": "Electronics",
       "list_price": 15000.00
     }'
```

### Crear Descuento por Tipo de Producto
```bash
curl -X POST "http://localhost:8000/discounts/product" \
     -H "Content-Type: application/json" \
     -d '{
       "product_type": "Electronics",
       "discount_percent": 5.0
     }'
```

### Crear Descuento por Método de Pago
```bash
curl -X POST "http://localhost:8000/discounts/payment" \
     -H "Content-Type: application/json" \
     -d '{
       "payment_method": "Cash",
       "discount_percent": 5.0
     }'
```

### Crear una Venta
```bash
curl -X POST "http://localhost:8000/sales/" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": 1,
       "payment_method": "Store Credit",
       "items": [
         {
           "product_id": 1,
           "quantity": 1
         }
       ]
     }'
```

## 💡 Lógica de Negocio

### Tipos de Cliente
- **VIP**: Términos de crédito extendidos (hasta 365 días)
- **Regular**: Términos de crédito estándar (hasta 365 días)

### Descuentos Aplicados
1. **Por tipo de producto**: Descuento específico por categoría
2. **Por método de pago**: Descuento según forma de pago
3. **Por términos de crédito**: 1.9% adicional para "Store Credit"

### Cálculo de Impuestos
- Tasa de impuesto: 16% por defecto
- Se aplica sobre el subtotal después de descuentos

### Estructura de Respuesta de Venta
La respuesta incluye un breakdown detallado con:
- Líneas de productos con descuentos individuales
- Subtotal después de descuentos
- Impuestos calculados
- Total final
- Monto total de descuentos aplicados

## 🤝 Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Tu Nombre - [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Pydantic por la validación de datos
- La comunidad de Python por el soporte continuo
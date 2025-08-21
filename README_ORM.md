# API Sales System - Implementación con ORM

Esta es la implementación completa de la API Sales System usando SQLAlchemy ORM con MySQL.

## 🏗️ **Arquitectura Implementada**

### **Capas de la Aplicación:**
1. **`app/config/`** - Configuración y variables de entorno
2. **`app/database/`** - Modelos SQLAlchemy y conexión a la BD
3. **`app/repositories/`** - Capa de acceso a datos
4. **`app/services/`** - Lógica de negocio
5. **`app/routers/`** - Endpoints de la API
6. **`database/`** - Scripts de inicialización y migraciones

## 🚀 **Configuración Inicial**

### **1. Variables de Entorno**
Copia el archivo `env.example` a `.env` y configura tus credenciales:

```bash
cp env.example .env
```

Edita `.env` con tus datos de MySQL:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=sales_system
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
DEBUG=True
```

### **2. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **3. Crear Base de Datos**
```sql
CREATE DATABASE sales_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### **4. Inicializar la Base de Datos**
```bash
python database/init_database.py
```

## 📊 **Estructura de la Base de Datos**

### **Tablas Principales:**
- **`customer_type`** - Tipos de cliente (VIP/Regular)
- **`credit_terms`** - Términos de crédito en días
- **`customer`** - Clientes con relaciones
- **`product_type`** - Tipos de producto
- **`product`** - Productos con precios
- **`payment_method`** - Métodos de pago
- **`product_type_discount`** - Descuentos por tipo de producto
- **`payment_method_discount`** - Descuentos por método de pago
- **`sale`** - Ventas principales
- **`sale_item`** - Items de cada venta

### **Características:**
- ✅ **Soft deletes** en todas las tablas
- ✅ **Timestamps** automáticos
- ✅ **Relaciones** con foreign keys
- ✅ **Índices** para performance
- ✅ **Constraints** de validación

## 🔧 **Uso de la API**

### **Endpoints Disponibles:**

#### **Clientes:**
- `POST /customers` - Crear cliente
- `GET /customers` - Listar clientes (sin soft-deleted)

#### **Productos:**
- `POST /products` - Crear producto
- `GET /products` - Listar productos (sin soft-deleted)

#### **Descuentos:**
- `POST /discounts/product` - Descuento por tipo de producto
- `POST /discounts/payment` - Descuento por método de pago

#### **Ventas:**
- `POST /sales` - Crear venta con cálculo automático
- `GET /sales` - Listar ventas (sin soft-deleted)

## 🧪 **Testing**

### **Ejecutar Tests:**
```bash
pytest tests/ -v
```

### **Tests Disponibles:**
- ✅ Tests de clientes
- ✅ Tests de productos
- ✅ Tests de descuentos
- ✅ Tests de ventas

## 📈 **Migraciones con Alembic**

### **Crear Nueva Migración:**
```bash
alembic revision --autogenerate -m "Descripción del cambio"
```

### **Aplicar Migraciones:**
```bash
alembic upgrade head
```

### **Revertir Migración:**
```bash
alembic downgrade -1
```

## 🗄️ **Operaciones de Base de Datos**

### **Crear Tablas:**
```python
from app.database.connection import create_tables
create_tables()
```

### **Eliminar Tablas (solo desarrollo):**
```python
from app.database.connection import drop_tables
drop_tables()
```

### **Obtener Sesión:**
```python
from app.database.connection import get_db
db = next(get_db())
```

## 🔍 **Ejemplos de Uso**

### **Crear Cliente:**
```python
from app.repositories.customer_repository import CustomerRepository

customer_repo = CustomerRepository()
customer_data = {
    "name": "Ana García",
    "customer_type_id": 1,  # VIP
    "credit_terms_id": 3    # 90 días
}
customer = customer_repo.create(db, customer_data)
```

### **Crear Venta:**
```python
from app.services.sale_service import SaleService

sale_service = SaleService()
sale_data = {
    "customer_id": 1,
    "payment_method_id": 4,  # Store Credit
    "items": [
        {"product_id": 1, "quantity": 1}
    ]
}
sale = sale_service.create_sale(db, sale_data)
```

## 🚨 **Manejo de Errores**

### **Errores Comunes:**
- **Conexión a BD**: Verificar credenciales y que MySQL esté corriendo
- **Modelos no encontrados**: Ejecutar `python database/init_database.py`
- **Migraciones fallidas**: Verificar que la BD esté creada y accesible

### **Logs de Debug:**
```bash
DEBUG=True uvicorn main:app --reload
```

## 📁 **Estructura de Archivos**

```
api_sales_system/
├── app/
│   ├── config/              # Configuración
│   ├── database/            # Modelos y conexión
│   ├── repositories/        # Acceso a datos
│   ├── services/            # Lógica de negocio
│   └── routers/             # Endpoints
├── database/
│   ├── init_database.py     # Script de inicialización
│   ├── seeds/               # Datos de prueba
│   └── migrations/          # Scripts de migración
├── alembic/                 # Configuración de migraciones
├── tests/                   # Tests automatizados
├── .env                     # Variables de entorno
└── requirements.txt         # Dependencias
```

## 🎯 **Próximos Pasos**

1. **Configurar variables de entorno** en `.env`
2. **Crear la base de datos** en MySQL
3. **Ejecutar script de inicialización**
4. **Probar la API** con los endpoints
5. **Ejecutar tests** para validar funcionalidad

## 🤝 **Contribuir**

1. Crear rama para tu feature
2. Implementar cambios
3. Crear migración si es necesario
4. Ejecutar tests
5. Crear Pull Request

---

**¡La implementación con ORM está lista para usar!** 🎉

# 🚀 API Sales System

Sistema de API para gestión de ventas, clientes, productos y descuentos construido con FastAPI y SQLAlchemy ORM.

## ✨ Características

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy ORM**: Mapeo objeto-relacional robusto
- **MySQL**: Base de datos relacional
- **Alembic**: Migraciones de base de datos
- **Arquitectura modular**: Separación clara de responsabilidades
- **Validación de datos**: Con Pydantic
- **Documentación automática**: Swagger UI en `/docs`

## 🏗️ Arquitectura

```
app/
├── config/           # Configuración de la aplicación
├── database/         # Modelos y conexión a BD
├── models/           # Modelos Pydantic para API
├── repositories/     # Capa de acceso a datos
├── routers/          # Endpoints de la API
└── services/         # Lógica de negocio
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd api_sales_system
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus credenciales de MySQL
```

### 5. Configurar base de datos MySQL
Asegúrate de que MySQL esté corriendo en Docker:
```bash
# Verificar que MySQL esté corriendo
docker ps | grep mysql
```

### 6. Inicializar la base de datos
```bash
python init_db.py
```

## 🗄️ Base de Datos

### Estructura de Tablas
- `customer_type`: Tipos de cliente (VIP, Regular)
- `credit_terms`: Términos de crédito (30, 60, 90 días)
- `customer`: Clientes del sistema
- `product_type`: Tipos de producto
- `product`: Productos disponibles
- `payment_method`: Métodos de pago
- `product_type_discount`: Descuentos por tipo de producto
- `payment_method_discount`: Descuentos por método de pago
- `sale`: Ventas realizadas
- `sale_item`: Items de cada venta

### Inicialización
El script `init_db.py` crea automáticamente:
- Tipos de cliente: VIP, Regular
- Términos de crédito: 30, 60, 90 días
- Tipos de producto: Electronics, Clothing, Books
- Métodos de pago: Cash, Credit Card, Store Credit

## 🚀 Ejecutar la API

### Desarrollo
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 Endpoints de la API

### Clientes
- `POST /customers` - Crear cliente
- `GET /customers` - Listar clientes

### Productos
- `POST /products` - Crear producto
- `GET /products` - Listar productos

### Descuentos
- `POST /discounts/product` - Crear descuento por tipo de producto
- `POST /discounts/payment` - Crear descuento por método de pago

### Ventas
- `POST /sales` - Crear venta
- `GET /sales` - Listar ventas

## 🔧 Configuración

### Variables de Entorno (.env)
```env
# Configuración de la Aplicación
APP_NAME=API Sales System
APP_VERSION=1.0.0
DEBUG=true

# Configuración de la Base de Datos
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=sales_system
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_ROOT_PASSWORD=tu_root_password

# Configuración de CORS
CORS_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
```

## 🧪 Testing

### Ejecutar tests
```bash
pytest
```

### Ejecutar tests con coverage
```bash
pytest --cov=app
```

## 📊 Migraciones con Alembic

### Inicializar Alembic
```bash
alembic init alembic
```

### Crear migración
```bash
alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar migraciones
```bash
alembic upgrade head
```

### Revertir migración
```bash
alembic downgrade -1
```

## 🔍 Documentación de la API

Una vez que la API esté corriendo, puedes acceder a:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 📝 Ejemplos de Uso

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

### Crear una Venta
```bash
curl -X POST "http://localhost:8000/sales/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "payment_method": "Store Credit",
    "items": [
      {"product_id": 1, "quantity": 1}
    ]
  }'
```

## 🐛 Troubleshooting

### Error de conexión a MySQL
- Verifica que MySQL esté corriendo en Docker
- Confirma las credenciales en `.env`
- Asegúrate de que el puerto 3306 esté accesible

### Error de importación
- Verifica que el entorno virtual esté activado
- Ejecuta `pip install -r requirements.txt` nuevamente

### Error de tablas
- Ejecuta `python init_db.py` para crear las tablas
- Verifica que MySQL esté funcionando correctamente

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación de la API en `/docs`
2. Verifica los logs de la aplicación
3. Abre un issue en el repositorio

---

**¡Disfruta usando la API Sales System! 🎉**
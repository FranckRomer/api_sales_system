# API Sales System

Sistema de API para gestión de ventas desarrollado con FastAPI.

## 🚀 Características

- API RESTful con FastAPI
- Documentación automática con Swagger/OpenAPI
- Tipado estático con Python
- Endpoints básicos para gestión de items

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

- `GET /` - Mensaje de bienvenida
- `GET /items/{item_id}` - Obtener un item por ID

## 🧪 Pruebas

Para ejecutar las pruebas (cuando se implementen):
```bash
pytest
```

## 📝 Estructura del Proyecto

```
api_sales_system/
├── main.py              # Archivo principal de la aplicación
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
├── .gitignore          # Archivos a ignorar en Git
└── venv/               # Entorno virtual (no se incluye en Git)
```

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
- La comunidad de Python por el soporte continuo
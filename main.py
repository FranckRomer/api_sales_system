from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import customers, products, discounts, sales
from app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de API para gestión de ventas, clientes, productos y descuentos",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Incluir routers
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(discounts.router)
app.include_router(sales.router)

@app.get("/")
def read_root():
    """
    Endpoint raíz de la API
    """
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "customers": "/customers",
            "products": "/products", 
            "discounts": "/discounts",
            "sales": "/sales"
        }
    }

@app.get("/health")
def health_check():
    """
    Endpoint de verificación de salud de la API
    """
    return {"status": "healthy", "service": settings.APP_NAME}
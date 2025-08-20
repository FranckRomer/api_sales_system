from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import customers, products, discounts, sales

app = FastAPI(
    title="API Sales System",
    description="Sistema de API para gestión de ventas, clientes, productos y descuentos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "message": "Bienvenido a API Sales System",
        "version": "1.0.0",
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
    return {"status": "healthy", "service": "API Sales System"}
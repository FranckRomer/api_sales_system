import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class DatabaseSettings:
    """Configuración de la base de datos MySQL"""
    
    # Configuración de MySQL
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sales_system")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    
    # Configuración de conexión
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_COLLATION = "utf8mb4_unicode_ci"
    
    @property
    def database_url(self) -> str:
        """URL de conexión a la base de datos"""
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset={self.MYSQL_CHARSET}"
        )
    
    @property
    def database_url_sync(self) -> str:
        """URL de conexión síncrona para Alembic"""
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset={self.MYSQL_CHARSET}"
        )

class Settings:
    """Configuración general de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME = "API Sales System"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración de la base de datos
    database = DatabaseSettings()
    
    # Configuración de CORS
    CORS_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

# Instancia global de configuración
settings = Settings()

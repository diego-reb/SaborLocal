import os

class Config:
    # Configuración común para ambos entornos (Desarrollo y Producción)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Para desactivar las señales de modificaciones
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi_secreto')  # Llave secreta para sesiones

class DevelopmentConfig(Config):
    DEBUG = True
    # Aquí puedes especificar la URL de tu base de datos PostgreSQL en el entorno de desarrollo
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://usuario:contraseña@localhost/nombre_base_datos')

class ProductionConfig(Config):
    DEBUG = False
    # Aquí también especificas la URL para PostgreSQL, pero en el entorno de producción
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://usuario:contraseña@localhost/nombre_base_datos')

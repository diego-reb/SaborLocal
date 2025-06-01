class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/SaborLocal'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/SaborLocal' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

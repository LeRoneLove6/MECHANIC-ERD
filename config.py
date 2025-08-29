
class DevelopmentConfig: 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Hillzz%4069@localhost/mechanic_db'
    DEBUG = True
    CACHE_DEFAULT_TIMEOUT = 300

class TestingConfig:
    pass

class ProductionConfig:
    pass


import os

class Config(object):
    # Default Configuration
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://dev:revbotdev@localhost/myrevbot'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://dev:revbotdev@localhost/myrevbot')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

class ProductionConfig(Config):
    # Production specific configs
    pass


class DevelopmentConfig(Config):
    # Development environment specific configuration
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # Optionally add a test database hosted in memory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


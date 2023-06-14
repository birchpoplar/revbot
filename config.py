class Config(object):
    # Default Configuration
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://dev:revbotdev@localhost/myrevbot'

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


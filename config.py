# config.py

class Config:
    """Base configuration variables."""
    ENV = 'production'
    SECRET_KEY = 'zdeyns-testing-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DISCORD_CLIENT_ID = '1236201561127125114'
    DISCORD_CLIENT_SECRET = 'y8qSw1U2pAYm8p7LJISXHhQS5FZt_IlR'
    OAUTH_REDIRECT_URI = 'http://localhost:5000/auth/authorize'

    USE_SESSION_FOR_NEXT = True

    JWT_SECRET_KEY = 'another-secret-key'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    
    HOST = 'http://localhost'
    PORT = '5000'

class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    ENV = 'development'
    DEBUG = True
    HOST = 'http://localhost'
    PORT = '5000'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False

class TestingConfig(Config):
    """Testing configuration with testing enabled."""
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False

class ProductionConfig(Config):
    """Production configuration with debug disabled."""
    DEBUG = False

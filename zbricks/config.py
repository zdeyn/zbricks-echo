# config.py

import os, dotenv

class Config:
    """Base configuration variables."""
    dotenv.load_dotenv()
    # Useful defaults
    ENV = 'none'
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv('APP_SECRET_KEY', 'default-boring-secret-key')
    HOST = 'localhost'
    PORT = '5000'

    # TODO: Move extension-specific config to their respective bricks
    # TODO: Have extensions register their Development/Testing/Production config to their parent bricks
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration with testing enabled."""
    ENV = 'testing'
    TESTING = True
    # JWT_COOKIE_SECURE = False
    # JWT_COOKIE_CSRF_PROTECT = False

class ProductionConfig(Config):
    """Production configuration with debug disabled."""
    ENV = 'production'
    DEBUG = False
    # JWT_COOKIE_SECURE = True
    # JWT_COOKIE_CSRF_PROTECT = True

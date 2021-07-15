import os


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '1102f6527230e520d316c57e5e26743f')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True

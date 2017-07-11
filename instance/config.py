import os
from decouple import config

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config('DEV_SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = config('DEV_SECRET_KEY')

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = config('TESTING')
    SQLALCHEMY_DATABASE_URI = config('TESTING_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('TESTING_SQLALCHEMY_TRACK_MODIFICATIONS')
    DEBUG = config('TESTING_DEBUG')
    SERVER_NAME = config('TESTING_SERVER_NAME')

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

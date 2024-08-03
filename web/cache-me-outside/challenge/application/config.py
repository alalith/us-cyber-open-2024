import os

class Config(object):
    SECRET_KEY = os.urandom(50)
    REDIS_HOST = os.getenv("REDIS_HOST")

class ProductionConfig(Config):
    pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
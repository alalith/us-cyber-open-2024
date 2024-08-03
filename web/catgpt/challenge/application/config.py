import os
import string

class Config(object):
    SECRET_KEY = os.urandom(50)
    MODEL_DIR = "/app/application/model"
    UPLOAD_DIR = "/app/uploads"
    DEBUG = True

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
import os
import string

class Config(object):
    SECRET_KEY = os.urandom(50)
    UPLOAD_FOLDER = "/tmp"
    FIRMWARE = "/firmware.bin"
    FIRMWARE_FOLDER = "/app/assets/firmware_updates"
    PRIV_KEYPATH = "/app/assets/keys/private.pem"
    PUB_KEYPATH = "/app/assets/keys/public.pem"
    SECRET_RESET_CODE = "USCG{t3st_fl4g}"

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
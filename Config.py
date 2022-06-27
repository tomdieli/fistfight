from os import environ, urandom
from distutils.debug import DEBUG

from dotenv import load_dotenv


class Config(object):
    DATABASE_URL = environ.get('DATABASE_URL')
    REDIS_URL = environ.get('REDIS_URL')
    SECRET_KEY = urandom(12).hex()
    SESSION_COOKIE_SECURE = True
    

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    load_dotenv('envs/dev/.env')
    DEBUG = environ.get('DEBUG')
    DATABASE_URL = environ.get('DATABASE_URL')
    REDIS_URL = environ.get('REDIS_URL')
    SECRET_KEY = environ.get('SECRET_KEY')


class TestingConfig(DevelopmentConfig):
    TESTING = True
    SECRET_KEY = 'notsosecret'
    DATABASE_URL = 'postgresql://postgres:mysecretpassword@localhost/arena'

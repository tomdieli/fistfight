from distutils.debug import DEBUG


class Config(object):
    DEBUG = False
    TESTING = False
    

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'supersecret'
    DATABASE_URL = 'postgresql://postgres:mysecretpassword@localhost/arena'
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'postgresql://postgres:mysecretpassword@localhost/test_arena'

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = ''

    DATABASE_HOST = ''
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_DB = ''

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''

    UPLOAD_FOLDER = '/static/uploads'

    SQLALCHEMY_WARN_20 = 1

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = ''

    DATABASE_HOST = ''
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_DB = ''

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = ''


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = ''

    DATABASE_HOST = ''
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_DB = ''

    SQLALCHEMY_DATABASE_URI = ''

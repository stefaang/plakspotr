import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    MONGODB_SETTINGS = {
        'db': 'plakspotr',
        # 'host': os.environ['MONGODB_URL']
    }
    #REDIS_URL = os.environ['REDIS_URL']
    #REDIS_CHAN = 'chat'

    #CELERY_BROKER_URL = os.environ['CELERY_BROKER']
    #CELERY_RESULT_BACKEND = os.environ['CELERY_BROKER']

    GOOGLE_ID = os.environ['GOOGLE_ID']
    GOOGLE_SECRET = os.environ['GOOGLE_SECRET']

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

cfgs = {
    'default': Config,
    'product': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig,
    'devel': DevelopmentConfig
}
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'should-be-secret'


class DevelConfig(BaseConfig):
    SQLALCHEMY_ECHO = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class HerokuConfig(BaseConfig):
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', '')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')

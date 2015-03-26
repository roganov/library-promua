import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'should-be-secret'

class DevelConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')

class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
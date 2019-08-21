import os

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
basedir = os.path.abspath(os.path.dirname(__file__))

if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_DB:
    DATABASE_URI = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}'
else:
    DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
MAX_USERNAME_LENGTH = 80
DATE_OF_BIRTH_KEY = 'dateOfBirth'


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE_URI


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE_URI

import os
from datetime import timedelta

class SQLAlchemy_config():
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","mysql+pymysql://flask:quQ351dTx@1.34.134.247:3306/TEST")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 30
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    PTTLITE_PER_PAGE = os.environ.get('PTTLITE_PER_PAGE', 20)

class PymysqlConfig():
    host = '1.34.134.247'
    user = 'flask'
    password = 'quQ351dTx'
    db = 'PTTLite'
    charset = 'utf8'
    port = int(3306)

class Config():
    JWT_SECRET_KEY = 'fk6hcej67az355szr'
    JWT_TOKEN_LOCATION = ['headers', 'query_string']
    PROPAGATE_EXCEPTIONS = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int(465)
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('admin', 'kiwichen.dev@gmail.com')
    MAIL_MAX_EMAILS =int(10)
    MAIL_USERNAME = 'kiwichen.dev@gmail.com'
    MAIL_PASSWORD = 'VNCofnhM7VRfp6EutE8wxocWCqxp28yKmGLZV3Q5eV9xdBjKhGDAPn26n2TEWQ2f'
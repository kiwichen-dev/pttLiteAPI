import os
from datetime import timedelta

class SQLAlchemy_config():
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","mysql+pymysql://flask:quQ351dTx@1.34.134.247:31478/PTTLite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 30
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    PTTLITE_PER_PAGE = os.environ.get('PTTLITE_PER_PAGE', 20)

class Config():
    #JWT - General Options:
    JWT_SECRET_KEY = 'fk6hcej67az355szr'
    JWT_TOKEN_LOCATION = ['headers', 'query_string']
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = int(900)
    JWT_REFRESH_TOKEN_EXPIRES = int(86400)*int(30)
    JWT_ALGORITHM = 'HS256'

    #JWT - Header Options
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # JTW - Json Body Options
    JWT_JSON_KEY = 'access_token'
    JWT_REFRESH_JSON_KEY = 'refresh_token'

    #JWT - Logout
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int(465)
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('admin', 'kiwichen.dev@gmail.com')
    MAIL_MAX_EMAILS =int(10)
    MAIL_USERNAME = 'kiwichen.dev@gmail.com'
    MAIL_PASSWORD = 'VNCofnhM7VRfp6EutE8wxocWCqxp28yKmGLZV3Q5eV9xdBjKhGDAPn26n2TEWQ2f'

    SECRET_KEY = 'development'
    UPLOAD_FOLDER = './images'
    ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
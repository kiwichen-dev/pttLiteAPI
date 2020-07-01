import os

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
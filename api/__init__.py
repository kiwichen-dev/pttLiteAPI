from flask import flask
from flask_restful import Resource,Api
from pymysqlpool.pool import Pool
from config import PymysqlConfig


def getCursor():
    pool = Pool(
                host=PymysqlConfig.host,
                port=PymysqlConfig.port, 
                user=PymysqlConfig.user, 
                password=PymysqlConfig.password, 
                db=PymysqlConfig.db
                )
    pool.init()
    connection = pool.get_conn()
    return connection.cursor()

    return 
def create_app():
    app = flask(__name__)
    return app


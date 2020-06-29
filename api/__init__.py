from flask import Flask
from flask_restful import Resource,Api
from pymysqlpool.pool import Pool
from api.config import PymysqlConfig
from flask_sqlalchemy import SQLAlchemy
from api.config import SQLAlchemy_config

db = SQLAlchemy()

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

from api.route import index, article, search, all_board, user

def create_app():
    app = Flask(__name__)
    app.config.from_object(SQLAlchemy_config)
    db.init_app(app)
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/<board>','board', all_board)
    app.add_url_rule('/<board>/<article_number>','article',article)
    #app.add_url_rule('/<bbs>/<board>/<page>', 'article', article)
    app.add_url_rule('/search', 'search', search, methods=['GET','POST'])
    app.add_url_rule('/user/<username>', 'user', user, methods=['GET','POST'])
    return app
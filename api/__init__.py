from flask import Flask
from flask_restful import Resource,Api
from pymysqlpool.pool import Pool
from api.config import PymysqlConfig
from flask_sqlalchemy import SQLAlchemy
from api.config import SQLAlchemy_config

db = SQLAlchemy()

def connection():
    pool = Pool(
                host=PymysqlConfig.host,
                port=PymysqlConfig.port, 
                user=PymysqlConfig.user, 
                password=PymysqlConfig.password, 
                db=PymysqlConfig.db
                )
    pool.init()
    pool.get_conn()
    return pool.get_conn()

from api.resource.user import User
from api.resource.boardArticle import Index,All_board,Article,Board,BoardToList
from flask.json import JSONEncoder
from datetime import date

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    api = Api(app)
    app.config.from_object(SQLAlchemy_config)
    db.init_app(app)
    api.add_resource(Index,'/')
    api.add_resource(All_board)
    api.add_resource(Board,'/board/<string:board_name>')
    api.add_resource(Article,'/<string:board>/<string:article_number>')
    api.add_resource(User,'/user/<string:username>')
    api.add_resource(BoardToList,'/boardtolist')
    """
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/<board>','board', all_board)
    app.add_url_rule('/<board>/<article_number>','article',article)
    app.add_url_rule('/search', 'search', search, methods=['GET','POST'])
    app.add_url_rule('/user/<username>', 'user', user, methods=['GET','POST'])
    """
    return app
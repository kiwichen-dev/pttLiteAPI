from flask import Flask
from flask_restful import Resource,Api
from pymysqlpool.pool import Pool
from api.config import PymysqlConfig
from flask_sqlalchemy import SQLAlchemy

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

from api.resource.user import User,Login,Protected,FollowBoard,FollowArticle,GetFollowingArticle,GetFollowingBoard
from api.resource.boardArticle import Index,All_board,Article,Board,BoardToList
from datetime import date
from api.config import SQLAlchemy_config
from api.model.JSONEncoder import CustomJSONEncoder
from api.model.user import UserModel
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.json_encoder = CustomJSONEncoder
    api = Api(app)
    app.config.from_object(SQLAlchemy_config)
    db.init_app(app)
    jwt = JWTManager(app)
    api.add_resource(Index,'/')
    api.add_resource(All_board)
    api.add_resource(Board,'/board/<string:board_name>')
    api.add_resource(Article,'/<string:board>/<string:article_number>')
    api.add_resource(User,'/user/<string:username>')
    api.add_resource(BoardToList,'/boardtolist')
    api.add_resource(Login,'/login')
    api.add_resource(Protected,'/protected')
    api.add_resource(FollowBoard,'/follow/<string:board>')
    api.add_resource(GetFollowingBoard,'/following_board')
    api.add_resource(FollowArticle,'/follow/<string:board>/<string:article_number>')
    api.add_resource(GetFollowingArticle,'/following_article')
    return app
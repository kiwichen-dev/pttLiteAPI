from flask import Flask,jsonify
from pymysqlpool.pool import Pool
from api.config import PymysqlConfig,Config
#from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api.model.JSONEncoder import CustomJSONEncoder
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS
from flask_mail import Mail
from time import time
"""
from flask_uploads import UploadSet, IMAGES, configure_uploads
"""

class InintAPP():
    #def sqlalchemy(self):
    #    return SQLAlchemy()

    def __init__(self):
        #self.db = SQLAlchemy()
        self.app = Flask(__name__)
        self.app.json_encoder = CustomJSONEncoder
        self.app.config.from_object(Config)
        CORS(self.app)
        self.mail = Mail(self.app)
        self.mail.init_app(self.app)
        self.api = Api(self.app)
        #db.init_app(self.app)
        self.jwt = JWTManager(self.app)
        """
        self.upload = UploadSet(name='def', extensions=IMAGES)
        self.configure_uploads(app, self.upload)
        """
        self.gossiping = None
        self.stock = None
        self.nba = None
        self.baseball = None
        self.c_chat = None

    def connection(self):
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

    # def refreshBoards(self,board_name):
    #     db = self.connection()
    #     cursor = db.cursor()
    #     sql = "SELECT * FROM articles WHERE board_name = '%s'" % (board_name)
    #     cursor.execute(sql)
    #     query_result = cursor.fetchall()
    #     if query_result:
    #         package = dict()
    #         package['board'] = query_result
    #         db.close()
    #         cursor.close()
    #         return jsonify(package)
    #     else:
    #         db.close()
    #         cursor.close()
    #         return None

from api.resource.user import Register,Login,Protected,FollowBoard,FollowArticle,GetFollowingArticles,GetFollowingBoards,Discuss,Reply,ForgotPassword,ResetPassword,Refresh_token,UploadImg
from api.resource.boardArticle import Index,All_board,Article,Board,BoardToList,Article_Left_Join

class App(InintAPP):
    def create_app(self):
        self.api.add_resource(Index,'/index')
        self.api.add_resource(All_board)
        self.api.add_resource(Board,'/board/<string:board_name>')
        self.api.add_resource(Article,'/<string:board>/<string:article_number>')
        self.api.add_resource(Article_Left_Join,'/left_join/<string:board>/<string:article_number>')
        self.api.add_resource(Register,'/register')
        self.api.add_resource(BoardToList,'/boardtolist')
        self.api.add_resource(Login,'/login')
        self.api.add_resource(Protected,'/protected')
        self.api.add_resource(FollowBoard,'/follow/<string:board_name>')
        self.api.add_resource(GetFollowingBoards,'/following_boards')
        self.api.add_resource(FollowArticle,'/follow/<string:board_name>/<string:article_number>')
        self.api.add_resource(GetFollowingArticles,'/following_articles')
        self.api.add_resource(Discuss,'/discuss')
        self.api.add_resource(Reply,'/reply')
        self.api.add_resource(ForgotPassword,'/forgotpassword')
        self.api.add_resource(ResetPassword,'/resetpassword/<token>')
        self.api.add_resource(Refresh_token,'/refresh_toekn')
        self.api.add_resource(UploadImg,'/upload_img')      
        return self.app
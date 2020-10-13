from flask import Flask, jsonify
from pymysqlpool.pool import Pool
from api.config import PymysqlConfig, Config
#from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api.model.JSONEncoder import CustomJSONEncoder
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from time import time
import string
import random
"""
from flask_uploads import UploadSet, IMAGES, configure_uploads
"""

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config.from_object(Config)
CORS(app)
mail = Mail(app)
mail.init_app(app)
api = Api(app)
jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

class InintAPP():
    def __init__(self):
        self.gossiping = None
        self.stock = None
        self.nba = None
        self.baseball = None
        self.c_chat = None

    @staticmethod
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

    @property
    def random_user_id(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))

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

from api.resource.user import Login, FollowBoard, FollowArticle, GetFollowingArticles, GetFollowingBoards, Discuss,\
    Reply, ForgotPassword, ResetPassword,ChangePassword, RefreshToken, UploadImg, MemberCenter, LogoutAccessToken, LogoutRefreshToken
from api.resource.boardArticle import Index, AllBoards, ArticlePage, Board

class App(InintAPP):
    @staticmethod
    def create_app():  # 使用靜態方法，可省略實體化，因此該方法不用self
        api.add_resource(Index, '/index')
        api.add_resource(AllBoards,'/boards')
        api.add_resource(Board, '/board/<string:board_name>')
        api.add_resource(ArticlePage, '/<string:board_name>/<string:article_number>')
        # api.add_resource(Article_Left_Join,'/left_join/<string:board>/<string:article_number>')
        # api.add_resource(Register,'/register')
        # api.add_resource(BoardToList,'/boardtolist')
        api.add_resource(Login, '/login')
        api.add_resource(FollowBoard, '/follow/<string:board_name>')
        api.add_resource(GetFollowingBoards,'/following_boards')
        api.add_resource(FollowArticle, '/follow/<string:board_name>/<string:article_number>')
        api.add_resource(GetFollowingArticles,'/following_articles')
        api.add_resource(Discuss, '/discuss')
        api.add_resource(Reply, '/reply')
        api.add_resource(ForgotPassword, '/forgotpassword')
        api.add_resource(ResetPassword, '/resetpassword/<token>')
        api.add_resource(ChangePassword,'/change_password')
        api.add_resource(RefreshToken, '/refresh_toekn')
        api.add_resource(UploadImg, '/upload_img')
        api.add_resource(MemberCenter, '/member_center')
        api.add_resource(LogoutAccessToken, '/logout_access_token')
        api.add_resource(LogoutRefreshToken, '/logout_refresh_token')
        return app

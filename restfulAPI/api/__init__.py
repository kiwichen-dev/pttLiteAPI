from flask import Flask, jsonify
# from pymysqlpool.pool import Pool
import pymysql.cursors
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
# pool = Pool(
#     host=PymysqlConfig.host,
#     port=PymysqlConfig.port,
#     user=PymysqlConfig.user,
#     password=PymysqlConfig.password,
#     db=PymysqlConfig.db
# )
# pool.init()


blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

class InitAPP():
    def __init__(self):
        self.mysql_offline = int(0)
        self.mysql_is_working = int(1)
        self.mysql_error = int(2)
        self.request_sucess = int(3)
        self.request_not_found = int(4)
        self.valid = int(5)
        self.invalid = int(6)  
        self.mysql_respon = dict()
        self.mysql_respon['respon_code'] = None
        self.mysql_respon['respon_content'] = None
    
    @staticmethod
    def connection():
        connection = pymysql.connect(
        host=PymysqlConfig.host,
        port=PymysqlConfig.port,
        user=PymysqlConfig.user,
        password=PymysqlConfig.password,
        db=PymysqlConfig.db,
        cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    # @staticmethod
    # def pool():
    #     try:
    #         pool = Pool(
    #             host=PymysqlConfig.host,
    #             port=PymysqlConfig.port,
    #             user=PymysqlConfig.user,
    #             password=PymysqlConfig.password,
    #             db=PymysqlConfig.db
    #         )
    #         pool.init()
    #     except:
    #         print('MySQL連線失敗')
    #         return None
    #     else:
    #         return pool
    @property
    def random_user_id(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def analysis_return(self,res):
        if res['respon_code'] == self.request_sucess:
            return {'msg':'Sucess'},201
        elif res['respon_code'] == self.request_not_found:
            return {'msg':'Not found'},404
        elif res['respon_code'] == self.mysql_offline:
            return {'msg':'MySQL offline'},500
        elif res['respon_code'] == self.mysql_error:
            return {'msg':'MySQL error'},500
        else:
            return {'msg':'Get an error'},500

    def db_commit_rollback(self,res):
        if res['respon_code'] == self.request_sucess:
            # pool = self.pool()
            connection = self.connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
                    cursor.close()
                except:
                    try:
                        connection.rollback()
                        connection.close()
                        cursor.close()
                    except:
                        pass
                    else:
                        pass
                    finally:
                        pass
                    res['respon_code'] == self.mysql_error
                    return res
                else:
                    return res
            else:
                res['respon_code'] == self.mysql_offline
                return res
        return res #回傳respon_code不更動

    # def refreshBoards(self,board_name):
    #     # pool = self.pool()
    #     cursor = connection.cursor()
    #     sql = "SELECT * FROM articles WHERE board_name = '%s'" % (board_name)
    #     cursor.execute(sql)
    #     query_result = cursor.fetchall()
    #     if query_result:
    #         package = dict()
    #         package['board'] = query_result
    #         connection.close()
    #         cursor.close()
    #         return jsonify(package)
    #     else:
    #         connection.close()
    #         cursor.close()
    #         return None

from api.resource.user import Login, FollowBoard, FollowArticle, GetFollowingArticles, GetFollowingBoards, Discuss,\
    Reply, ForgotPassword, ResetPassword,ChangePassword, RefreshToken, UploadImg, MemberCenter, LogoutAccessToken, LogoutRefreshToken
from api.resource.boardArticle import Index, AllBoards, ArticlePage, Board, ArticleContent

class App(InitAPP):
    @staticmethod
    def create_app():  # 使用靜態方法，可省略實體化，因此該方法不用self
        api.add_resource(Index, '/index')
        api.add_resource(AllBoards,'/boards')
        api.add_resource(Board, '/board/<string:board_name>')
        api.add_resource(ArticlePage, '/<string:board_name>/<string:article_number>')
        api.add_resource(ArticleContent,'/article_content/<string:board_name>/<string:article_number>')
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

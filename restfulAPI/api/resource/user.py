from flask_restful import Resource, reqparse
from flask import request, current_app, jsonify
from api import InintAPP,check_if_token_in_blacklist,blacklist
import json
from api.model.user import UserModel
from api.model.boardArticle import LinkVaildate
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from werkzeug.datastructures import FileStorage
import os
import base64

class FollowBoard(UserModel,Resource):
    @jwt_required 
    def post(self,board_name):
        uuid = get_jwt_identity()
        if self.follow_board(uuid,board_name):
            return {'msg':'sucess'},201
        else:
            return {'msg':'board not found'},404

class FollowArticle(UserModel,Resource):
    @jwt_required 
    def post(self,board_name,article_number):
        uuid = get_jwt_identity()
        if self.follow_article(uuid,board_name,article_number):
            return {'msg':'sucess'},201
        else:
            return {'msg':'article not found'},404

class GetFollowingArticles(UserModel,Resource):
    @jwt_required
    def post(self):
        email = get_jwt_identity()
        followe_articles = dict()
        followe_articles['following_articles'] = self.get_following_articles(email)
        return jsonify(followe_articles),200

class GetFollowingBoards(UserModel,Resource):
    @jwt_required
    def post(self):
        email = get_jwt_identity()
        followe_boards = dict()
        followe_boards['following_articles'] = self.get_following_boards(email)
        return jsonify(followe_boards),200

class Login(UserModel,Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, required=True, help='required email'
        )
        parser.add_argument(
            'password', type = self.min_length_str(8), required=True,
            help='require password'
        )
        data = parser.parse_args()
        email = data['email']
        password = data['password']

        if self.isUser(email):
            vaildate = self.vaildate_password(email,password)
            if vaildate[0]:
                uuid = vaildate[1]
                self.login_records(uuid)
                return {
                    'access_token': create_access_token(identity=uuid),
                    'refresh_token': create_refresh_token(identity=uuid)
                }, 200
            else:
                return {'msg':'wrong of email or password '},401
        else:
            # parser = reqparse.RequestParser()
            # parser.add_argument(
            #     'email', type=str, required=True, help='required email'
            # )
            # parser.add_argument(
            #     'password', type = self.min_length_str(8), required=True,
            #     help='password error'
            # )
            # data = parser.parse_args()
            # email = data['email']
            # password = data['password']
            user_id = self.random_user_id
            db = self.connection()
            cursor = db.cursor()
            password_hash = self.set_password(password)
            sql = "INSERT INTO Users(email,nickname,pw,pw_hash,create_time,user_uuid) VALUES('{}','{}','{}','{}',now(),uuid())".format(email,user_id,password,password_hash)
            cursor.execute(sql)
            db.commit()
            sql = "SELECT user_uuid FROM Users WHERE nickname = '{}'".format(user_id)
            cursor.execute(sql)
            uuid = cursor.fetchone()['user_uuid']
            db.close()
            cursor.close()
            return {
                    'access_token': create_access_token(identity=uuid),
                    'refresh_token': create_refresh_token(identity=uuid)
                }, 201

# class Protected(Resource):
#     @jwt_required
#     def get(self):
#         identity = get_jwt_identity()
#         return {
#             'identity': identity
#         }, 200

# class Register(UserModel,Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument(
#             'email', type=str, required=True, help='required email'
#         )
#         parser.add_argument(
#             'username', type = self.min_length_str(4), required=True,
#             help='username require'
#         )
#         parser.add_argument(
#             'password', type = self.min_length_str(8), required=True,
#             help='password error'
#         )
#         data = parser.parse_args()
#         email = data['email']
#         username = data['username']
#         password = data['password']
#         db = self.connection()
#         cursor = db.cursor()
#         sql = "SELECT * FROM users WHERE nickname = '%s'" % (username)
#         cursor.execute(sql)
#         if cursor.fetchone():
#             cursor.close()
#             return {'message': 'user already exist'},401
#         else:
#             password_hash = self.set_password(password)
#             sql = "INSERT INTO users(nickname,email,pw,pw_hash) VALUES('%s','%s','%s','%s')" % (username,email,password,password_hash)
#             cursor.execute(sql)
#             db.commit()
#             cursor.close()
#             return {'message':'user has been created'}, 201

class ForgotPassword(UserModel,Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, required=True, help='required email'
        )
        data = parser.parse_args()
        email = data['email']
        if self.forgot_password(email):
            return {'message':'susscess'}, 201
        else:
            return {'message':'user not found'}, 400

class ResetPassword(UserModel,Resource):
    def get(self,token):
        if self.reset_password(token):
            return {'msg':'password changed!'},201
        else:
            return {'msg':'Link has revoked'},401

class ChangePassword(UserModel,Resource):
    @jwt_required
    def put(self):
        uuid = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument(
            'password', type = self.min_length_str(8), required=True,
            help='password require and length >= 8'
        )
        parser.add_argument(
            'repeat_password', type = self.min_length_str(8), required=True,
            help='password require and length >= 8'
        )
        data = parser.parse_args()
        password = data['password']
        repeat_password = data['repeat_password']

        if password == repeat_password:
            if self.change_password(uuid,password):
                return {'msg':'password changed!'},201
            else:
                return {'msg':'API error'},500
        else:
            return {'msg':'Make sure password equal repeat-password'},400

class Discuss(Resource,UserModel):
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument(
            'board_name', type=str, required=True, help='required board_name'
        )
        parser.add_argument(
            'article_number', type=str, required=True, help='required article_number'
        )
        parser.add_argument(
            'respone_type', type=str, required=True, help='required respone_type'
        )
        parser.add_argument(
            'discussion', type=str, required=True, help='required discussion'
        )
        parser.add_argument(
            'respone_user_ip', type=str, required=True, help='required respone_user_ip'
        )
        data = parser.parse_args()
        board_name = data['board_name']
        article_number = data['article_number']
        respone_type = data['respone_type']
        respone_user_id = self.get_user_by_uuid(uuid)['nickname']
        discussion = data['discussion']
        respone_user_ip = data['respone_user_ip']
        
        res = self.discuss(board_name,article_number,respone_type,respone_user_id,discussion,respone_user_ip)
        if res == self.request_sucess:
            return {'msg':'discussion submit'}, 201
        elif res == self.request_not_found:
            return {'msg':'Can not find the article'}, 404
        elif res == self.mysql_offline:
            return {'msg':'MySQL offline'},500
        else:
            return {'msg':'Got error'},500

    @jwt_required
    def put(self):
        pass

class Reply(Resource,UserModel,LinkVaildate):
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument(
            'nu', type=str, required=True, help='required nu'
        )
        parser.add_argument(
            'board_name', type=str, required=True, help='required board_name'
        )
        parser.add_argument(
            'article_number', type=str, required=True, help='required article_number'
        )
        parser.add_argument(
            'respone_type', type=str, required=True, help='required respone_type'
        )
        parser.add_argument(
            'reply', type=str, required=True, help='required reply'
        )
        parser.add_argument(
            'respone_user_ip', type=str, required=True, help='required respone_user_ip'
        )
        data = parser.parse_args()
        nu = data['nu']
        board_name = data['board_name']
        article_number = data['article_number']
        respone_type = data['respone_type']
        respone_user_id = self.get_user_by_uuid(uuid)['nickname']
        reply = data['reply']
        respone_user_ip = data['respone_user_ip']

        res = self.reply(nu,board_name,article_number,respone_type,respone_user_id,reply,respone_user_ip)
        if res == self.request_sucess:
            return {'msg':'reply submit'}, 201
        elif res == self.request_not_found:
            return {'msg':'Can not find the article'}, 404
        elif res == self.mysql_offline:
            return {'msg':'MySQL offline'}, 500
        else:
            return {'msg':'Got error'},500

class RefreshToken(UserModel,Resource):
    @jwt_refresh_token_required
    def post(self):
        uuid = get_jwt_identity()
        token = self.refresh_token(uuid)
        if token:
            return token,200
        else:
            return {'msg':'invaild token'},401

class UploadImg(UserModel,Resource):
    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('imgFile', required=True, type=FileStorage,location='files',help="imgFile is wrong.")
        
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        if self.uploadFiles(uuid):
            return {'msg':'sucess'}, 201
        else:
            return {'msg':'png,jpg,jpeg only'}, 400

    #     email = get_jwt_identity()
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('userIcon', required=True, type=FileStorage,location='files',help="imgFile is wrong.")
    #     img_file = parser.parse_args().get('userIcon')
    #     if self.is_allowed_file(img_file):
    #         dirname = 'imgs/{}/icon'.format(email)
    #         os.makedirs(dirname,mode=0o777,exist_ok=True)
    #         save_path = os.path.join(dirname, img_file.filename)
    #         img_file.save(save_path)
    #         return {'msg':'sucess'}, 201
    #     else:
    #         return {'msg':'png,jpg,jpeg only'}, 400
    
    # def is_allowed_file(self,uploadFile):
    #     if '.' in uploadFile.filename:
    #         ext = uploadFile.filename.rsplit('.', 1)[1].lower()
    #         if ext in {'png','jpg', 'jpeg'}:
    #             return True
    #     else:
    #         return False

class MemberCenter(UserModel,Resource):
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        return jsonify( self.member_data(uuid) )

class LogoutAccessToken(UserModel,Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"msg": "Successfully logged out"}, 200

class LogoutRefreshToken(UserModel,Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"msg": "Successfully logged out"}, 200
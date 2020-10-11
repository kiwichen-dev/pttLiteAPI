from flask_restful import Resource, reqparse
from flask import request, current_app, jsonify
from api import InintAPP,check_if_token_in_blacklist,blacklist
import json
from api.model.user import UserModel,min_length_str
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
        email = get_jwt_identity()
        if self.follow_board(email,board_name):
            return {'msg':'sucess'},201
        else:
            return {'msg':'error'},401

class FollowArticle(UserModel,Resource):
    @jwt_required 
    def post(self,board_name,article_number):
        email = get_jwt_identity()
        if self.follow_article(email,board_name,article_number):
            return {'msg':'sucess'},201
        else:
            return {'msg':'error'},401

class GetFollowingArticles(UserModel,Resource):
    @jwt_required
    def post(self):
        email = get_jwt_identity()
        followe_articles = dict()
        followe_articles['following_articles'] = self.get_following_articles(email)
        return jsonify(followe_articles)

class GetFollowingBoards(UserModel,Resource):
    @jwt_required
    def post(self):
        email = get_jwt_identity()
        followe_boards = dict()
        followe_boards['following_articles'] = self.get_following_boards(email)
        return jsonify(followe_boards)

class Login(UserModel,Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, required=True, help='required email'
        )
        parser.add_argument(
            'password', type = min_length_str(8), required=True,
            help='require password'
        )
        data = parser.parse_args()
        email = data['email']
        password = data['password']

        if self.isUser(email):
            if self.vaildate_password(email,password):
                return {
                    'access_token': create_access_token(identity=email),
                    'refresh_token': create_refresh_token(identity=email)
                }, 200
            else:
                return {'msg':'wrong of email or password '},401
        else:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'email', type=str, required=True, help='required email'
            )
            # parser.add_argument(
            #     'username', type = min_length_str(4), required=True,
            #     help='username require'
            # )
            parser.add_argument(
                'password', type = min_length_str(8), required=True,
                help='password error'
            )
            data = parser.parse_args()
            email = data['email']
            # username = data['username']
            password = data['password']
            db = self.connection()
            cursor = db.cursor()
            password_hash = self.set_password(password)
            sql = "INSERT INTO users(email,pw,pw_hash) VALUES('{}','{}','{}')".format(email,password,password_hash)
            cursor.execute(sql)
            db.commit()
            db.close()
            cursor.close()
            return {
                    'access_token': create_access_token(identity=email),
                    'refresh_token': create_refresh_token(identity=email)
                }, 201

class Protected(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        return {
            'identity': identity
        }, 200

class Register(UserModel,Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, required=True, help='required email'
        )
        parser.add_argument(
            'username', type = min_length_str(4), required=True,
            help='username require'
        )
        parser.add_argument(
            'password', type = min_length_str(8), required=True,
            help='password error'
        )
        data = parser.parse_args()
        email = data['email']
        username = data['username']
        password = data['password']
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE nickname = '%s'" % (username)
        cursor.execute(sql)
        if cursor.fetchone():
            cursor.close()
            return {'message': 'user already exist'},401
        else:
            password_hash = self.set_password(password)
            sql = "INSERT INTO users(nickname,email,pw,pw_hash) VALUES('%s','%s','%s','%s')" % (username,email,password,password_hash)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            return {'message':'user has been created'}, 201

class ForgotPassword(UserModel,Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', type=str, required=True, help='required email'
        )
        data = parser.parse_args()
        email = data['email']
        if self.forgot_password(email):
            return {'message':'susscess'}, 201
        else:
            return {'message':'user not found'}, 401

class ResetPassword(UserModel,Resource):
    def get(self,token):
        if self.reset_password(token):
            return 201
        else:
            return 401

class Discuss(Resource,UserModel,LinkVaildate):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'article_number', type=str, required=True, help='required article_number'
        )
        parser.add_argument(
            'respone_type', type=str, required=True, help='required respone_type'
        )
        parser.add_argument(
            'respone_user_id', type=str, required=True, help='required respone_user_id'
        )
        parser.add_argument(
            'discuss', type=str, required=True, help='required discuss'
        )
        parser.add_argument(
            'respone_user_ip', type=str, required=True, help='required respone_user_ip'
        )
        parser.add_argument(
            'board_name', type=str, required=True, help='required board_name'
        )
        data = parser.parse_args()
        article_number = data['article_number']
        respone_type = data['respone_type']
        respone_user_id = data['respone_user_id']
        discussion = data['discussion']
        respone_user_ip = data['respone_user_ip']
        board_name = data['board_name']

        if self.check_Discussion(board_name,article_number):
            self.discuss(article_number,respone_type,respone_user_id,discussion,respone_user_ip,board_name)
            return {'message':'discussion submit'}, 201
        else:
            return {'message':'Can not find the article'}, 400

class Reply(Resource,UserModel,LinkVaildate):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'article_discussion_id', type=str, required=True, help='required article_discussion_id'
        )
        parser.add_argument(
            'article_number', type=str, required=True, help='required article_number'
        )
        parser.add_argument(
            'respone_type', type=str, required=True, help='required respone_type'
        )
        parser.add_argument(
            'respone_user_id', type=str, required=True, help='required respone_user_id'
        )   
        parser.add_argument(
            'discuss', type=str, required=True, help='required discuss'
        )
        parser.add_argument(
            'respone_user_ip', type=str, required=True, help='required respone_user_ip'
        )
        parser.add_argument(
            'board_name', type=str, required=True, help='required board_name'
        )
        data = parser.parse_args()
        article_discussion_id = data['article_discussion_id']
        article_number = data['article_number']
        respone_type = data['respone_type']
        respone_user_id = data['respone_user_id']
        discussion = data['discussion']
        respone_user_ip = data['respone_user_ip']
        board_name = data['board_name']

        if self.check_Reply(board_name,article_number,article_discussion_id):
            self.reply(article_discussion_id,article_number,respone_type,respone_user_id,discussion,respone_user_ip,board_name)
            return {'message':'reply submit'}, 201
        else:
            return {'message':'Can not find the article'}, 400

class Refresh_token(UserModel,Resource):
    @jwt_refresh_token_required
    def post(self):
        email = get_jwt_identity()
        token = self.refresh_token(email)
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
        email = get_jwt_identity()
        if self.uploadFiles(email):
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
        email = get_jwt_identity()
        return jsonify( self.member_data(email) )

# class Logout():
#     def __init__(self):
#         self.blacklist = set()

#     @jwt.token_in_blacklist_loader
#     def check_if_token_in_blacklist(decrypted_token):
#         jti = decrypted_token['jti']
#         return jti in self.blacklist

class LogoutAccessToken(UserModel,Resource):
    @jwt_required
    def post(self):
        print('acc ok')
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"msg": "Successfully logged out"}, 200

class LogoutRefreshToken(UserModel,Resource):
    @jwt_refresh_token_required
    def post(self):
        print('refresh ok')
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"msg": "Successfully logged out"}, 200
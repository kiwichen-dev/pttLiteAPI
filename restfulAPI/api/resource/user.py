from flask_restful import Resource, reqparse
from flask import request, current_app
from api import connection
import json
from api.model.user import UserModel
from api.model.boardArticle import LinkCheck
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

def min_length_str(min_length):
    def validate(s):
        if s is None:
            raise Exception('password required')
        if not isinstance(s, (int, str)):
            raise Exception('password format error')
        s = str(s)
        if len(s) >= min_length:
            return s
        raise Exception("String must be at least %i characters long" % min_length)
    return validate

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email', type=str, required=True, help='required email'
    )
    parser.add_argument(
        'password', type=min_length_str(8), required=True,
        help='password error'
    )

    def get(self):
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE nickname = '%s'" % (username)
        cursor.execute(sql)
        if cursor.fetchone():
            return {'message':'user already exist'}
        else:
            return {'message': 'user not found'},204
    
    @jwt_required
    def booking(self):
        return {"message":"token is working"},201
    
    """
    def delete(self, username):
        user = UserModel.get_by_username(username)
        if user:
            user.delete()
            return {'message': 'user deleted'}
        else:
            return {'message': 'user not found'}, 204
    
    def put(self, username):
        user = UserModel.get_by_username(username)
        if user:
            data = User.parser.parse_args()
            user.password_hash = data['password']
            user.update()
            return user.as_dict()
        else:
            return {'message': "user not found"}, 204    
    """

class FollowBoard(UserModel,Resource):
    @jwt_required 
    def post(self,board):
        email = get_jwt_identity() #這行如果驗證錯誤自己會reject
        if self.follow_board(email,board) == True:
            return {'msg':'done'},200
        else:
            return {'msg':'error'},422

class FollowArticle(UserModel,Resource):
    @jwt_required 
    def post(self,board,article_number):
        email = get_jwt_identity() #這行如果驗證錯誤自己會reject
        if self.follow_article(email,board,article_number) == True:
            return {'msg':'done'},200
        else:
            return {'msg':'error'},422

class GetFollowingArticle(UserModel,Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        return self.get_following_article(email)

class GetFollowingBoard(UserModel,Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        return self.get_following_board(email)

class Login(UserModel,Resource):
    def post(self):
        data = User.parser.parse_args()
        email = data['email']
        password = data['password']
        self.check_password(email,password)
        if self.check_password(email,password) == True:
            access_token = create_access_token(identity=email)
            return {
                'access_token': access_token
            }, 200

class Register(User,UserModel,Resource):
    def post(self):
        self.parser.add_argument(
            'username', type=str, required=True, help='required username'
        )
        data = self.parser.parse_args()
        email = data['email']
        username = data['username']
        password = data['password']
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE nickname = '%s'" % (username)
        cursor.execute(sql)
        if cursor.fetchone():
            cursor.close()
            return {'message': 'user already exist'}
        else:
            password_hash = self.set_password(password)
            sql = "INSERT INTO user(nickname,email,pw,pw_hash) VALUES('%s','%s','%s','%s')" % (username,email,password,password_hash)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            return {'message':'user has been created'}, 201


class Protected(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        return {
            'identity': identity
        }, 200

class Disscuss(Resource,UserModel,LinkCheck):
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
            'disscuss', type=str, required=True, help='required disscuss'
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
        disscuss = data['disscuss']
        respone_user_ip = data['respone_user_ip']
        board_name = data['board_name']

        if self.check_Disscussion(board_name,article_number):
            self.disscuss(article_number,respone_type,respone_user_id,disscuss,respone_user_ip,board_name)
            return {'message':'disscussion submit'}, 201
        else:
            return {'message':'Can not find the article'}, 400

class Reply(Resource,UserModel,LinkCheck):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'article_disscussion_id', type=str, required=True, help='required article_disscussion_id'
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
            'disscuss', type=str, required=True, help='required disscuss'
        )
        parser.add_argument(
            'respone_user_ip', type=str, required=True, help='required respone_user_ip'
        )
        parser.add_argument(
            'board_name', type=str, required=True, help='required board_name'
        )
        data = parser.parse_args()
        article_disscussion_id = data['article_disscussion_id']
        article_number = data['article_number']
        respone_type = data['respone_type']
        respone_user_id = data['respone_user_id']
        disscuss = data['disscuss']
        respone_user_ip = data['respone_user_ip']
        board_name = data['board_name']

        if self.check_Reply(board_name,article_number,article_disscussion_id):
            self.reply(article_disscussion_id,article_number,respone_type,respone_user_id,disscuss,respone_user_ip,board_name)
            return {'message':'reply submit'}, 201
        else:
            return {'message':'Can not find the article'}, 400
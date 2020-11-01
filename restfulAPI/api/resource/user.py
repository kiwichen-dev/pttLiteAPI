from flask_restful import Resource, reqparse
from flask import request, current_app, jsonify
from api import InitAPP,check_if_token_in_blacklist,blacklist
import json
from api.model.user import UserModel
from api.model.boardArticle import LinkValidate
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
        res = self.follow(uuid,board_name)
        return self.analysis_return(res)
    @jwt_required 
    def delete(self,board_name):
        uuid = get_jwt_identity()
        res = self.unfollow(uuid,board_name)
        return self.analysis_return(res)

class FollowArticle(UserModel,Resource):
    @jwt_required 
    def post(self,board_name,article_number):
        uuid = get_jwt_identity()
        res = self.follow(uuid,board_name,article_number)
        return self.analysis_return(res)
    @jwt_required 
    def delete(self,board_name,article_number):
        uuid = get_jwt_identity()
        res = self.unfollow(uuid,board_name,article_number)
        return self.analysis_return(res)

class Following(UserModel,Resource):
    @jwt_required
    def get(self):
        uuid = get_jwt_identity()
        following = dict()
        following['following_boards'] = self.get_following_boards(uuid)
        following['following_articles'] = self.get_following_articles(uuid)
        return jsonify(following)

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
        is_user = self.isUser(email)
        if is_user['respon_code'] == self.resource_found:
            res = self.validate_password(email,password)
            if res['respon_code'] == self.valid:
                uuid = res['respon_content']
                self.login_records(uuid)
                # user_privileges =  self.user_privileges(uuid)
                # identity = list()
                # identity.append(uuid)
                # identity.append(user_privileges)
                return {
                    'access_token': create_access_token(identity=uuid),
                    'refresh_token': create_refresh_token(identity=uuid)
                }, 200
            else:
                return self.analysis_return(res)
        elif is_user['respon_code'] == self.resource_not_found:
            user_id = self.random_user_id
            connection = self.connection()
            cursor = connection.cursor()
            password_hash = self.set_password(password)
            sql = "INSERT INTO Users(email,nickname,pw,pw_hash,user_privileges,create_time,user_uuid) VALUES('{}','{}','{}','{}','user',now(),uuid())".format(email,user_id,password,password_hash)
            cursor.execute(sql)
            connection.commit()
            sql = "SELECT user_uuid FROM Users WHERE nickname = '{}'".format(user_id)
            cursor.execute(sql)
            uuid = cursor.fetchone()['user_uuid']
            connection.close()
            return {
                    'access_token': create_access_token(identity=uuid),
                    'refresh_token': create_refresh_token(identity=uuid)
                }, 201
        else:
            return self.analysis_return(is_user)

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

class Discuss(UserModel,Resource):
    @jwt_required
    def get(self):
        uuid = get_jwt_identity()
        return jsonify(self.my_discussions(uuid))
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
        res = self.discuss_or_reply(board_name,article_number,respone_type,respone_user_id,discussion,respone_user_ip)
        return self.analysis_return(res)
    @jwt_required
    def put(self):
        pass

class Reply(UserModel,Resource):
    @jwt_required
    def get(self):
        uuid = get_jwt_identity()
        return jsonify(self.my_reply(uuid))

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
        res = self.discuss_or_reply(nu,board_name,article_number,respone_type,respone_user_id,reply,respone_user_ip)
        return self.analysis_return(res)

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
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        if self.uploadFiles(uuid):
            return {'msg':'sucess'}, 201
        else:
            return {'msg':'png,jpg,jpeg only'}, 400

class MemberCenter(UserModel,Resource):
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        return jsonify(self.member_data(uuid))

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
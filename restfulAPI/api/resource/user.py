from flask_restful import Resource, reqparse
from flask import request, current_app
from api import connection
import json
#from flask_jwt import jwt_required
#from restdemo.model.user import User as UserModel

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
        'password', type=min_length_str(8), required=True,
        help='password error'
    )
    parser.add_argument(
        'email', type=str, required=True, help='required email'
    )

    def get(self, username):
        print(username)
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE nickname = '%s'" % (username)
        cursor.execute(sql)
        if cursor.fetchone():
            return {'message':'user exist'}
        else:
            return {'message': 'user not found'}, 404

    def post(self, username):
        data = User.parser.parse_args()
        email = data['email']
        pw = data['password']
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE nickname = '%s'" % (username)
        cursor.execute(sql)
        if cursor.fetchone():
            cursor.close()
            return {'message': 'user already exist'}
        else:
            sql = "INSERT INTO user(nickname,email,pw) VALUES('%s','%s','%s')" % (username,email,pw)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            return {'message':'user has been created'}, 201
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


class UserList(Resource):

    @jwt_required()
    def get(self):
        users = UserModel.get_user_list()
        return [u.as_dict() for u in users]
    """

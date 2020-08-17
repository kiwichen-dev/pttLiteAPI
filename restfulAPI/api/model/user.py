from datetime import datetime, timedelta
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from api import Database

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_mail import Message
from flask_restful import Resource, reqparse

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

class UserModel(Database):
    def __init__(self):
        self.parser = reqparse.RequestParser()
    """
    def get(self):
        db = self.connection()
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
    
    def set_password(self,password):
        return generate_password_hash(password)

    def check_password(self,email,password):
        sql = "SELECT pw_hash FROM user WHERE email = '%s'" % (email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        password_hash = cursor.fetchone()['pw_hash']
        return check_password_hash(password_hash,password)

    @staticmethod
    def get_by_username(username):
        sql = "SELECT * FROM user WHERE nickname = '%s'" % (username)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            return user

    @staticmethod
    def get_by_id(username):
        sql = "SELECT nickname FROM user WHERE nickname = '%s'" % (username)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    @staticmethod
    def get_user_list(username):
        sql = "SELECT nickname FROM user" % (username)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    def follow_board(self,email,board):
        sql = "UPDATE user SET bookmark ='%s' WHERE email = '%s'" % (board,email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True

    def follow_article(self,email,board,article_number):
        bookmark = board + article_number
        sql = "UPDATE user SET bookmark ='%s' WHERE email = '%s'" % (bookmark,email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        res = board + article + "已追蹤"
        return True

    def get_following_board(self,email):
        sql = "SELECT bookmark FROM user WHERE email = '%s'" % (email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def get_following_article(self,email):
        sql = "SELECT bookmark FROM user WHERE email = '%s'" % (email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
    def disscuss(self,article_number,respone_type,respone_user_id,disscuss,respone_user_ip,board_name):
        sql = \
        "INSERT INTO article_disscuss(\
            from_pttLite, \
            article_number,\
            respone_type,\
            respone_user_id,\
            disscuss,\
            respone_user_ip,\
            create_time,\
            last_update,\
            board_name\
            )\
        VALUES(true,'%s','%s','%s','%s','%s',NOW(),NOW(),'%s')" % (
            article_number,
            respone_type,
            respone_user_id,
            disscuss,
            respone_user_ip,
            board_name
        )
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

    def reply(self,article_disscussion_id,article_number,respone_type,respone_user_id,disscuss,respone_user_ip,board_name):
        sql = \
        "INSERT INTO reply_from_pttLite(\
            article_disscussion_id,\
            article_number,\
            respone_type,\
            respone_user_id,\
            disscuss,\
            respone_user_ip,\
            create_time,\
            last_update,\
            board_name\
            )\
        VALUES(%s,'%s','%s','%s','%s','%s',now(),now(),'%s')" % (
            article_disscussion_id,
            article_number,
            respone_type,
            respone_user_id,
            disscuss,
            respone_user_ip,
            board_name
        )
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    
    def forgot_password(self,email):
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE email = '%s'" % (email)
        cursor.execute(sql)
        if cursor.fetchone():
            msg_title = 'PTT Lite 重設密碼'
            msg_sender = 'kiwichen.dev@gmail.com'
            msg_recipients = [str(email)]
            msg_body = '密碼重設連結'
            msg_html = '<h1>密碼重設連結</h1>'
            msg = Message(msg_title,
                        sender=msg_sender,
                        recipients=msg_recipients)
            msg.body = msg_body
            msg.html = msg_html
            self.mail.send(msg)
            return True
        else:
            return False
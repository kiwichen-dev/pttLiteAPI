from datetime import datetime, timedelta
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from api import connection

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

class UserModel():
    def set_password(self,password):
        return generate_password_hash(password)

    def check_password(self,email,password):
        sql = "SELECT pw_hash FROM user WHERE email = '%s'" % (email)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        password_hash = cursor.fetchone()['pw_hash']
        return check_password_hash(password_hash,password)

    @staticmethod
    def get_by_username(username):
        sql = "SELECT * FROM user WHERE nickname = '%s'" % (username)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            return user

    @staticmethod
    def get_by_id(username):
        sql = "SELECT nickname FROM user WHERE nickname = '%s'" % (username)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    @staticmethod
    def get_user_list(username):
        sql = "SELECT nickname FROM user" % (username)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    def follow_board(self,email,board):
        sql = "UPDATE user SET bookmark ='%s' WHERE email = '%s'" % (board,email)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True

    def follow_article(self,email,board,article_number):
        bookmark = board + article_number
        sql = "UPDATE user SET bookmark ='%s' WHERE email = '%s'" % (bookmark,email)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        res = board + article + "已追蹤"
        return True

    def get_following_board(self,email):
        sql = "SELECT bookmark FROM user WHERE email = '%s'" % (email)
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def get_following_article(self,email):
        sql = "SELECT bookmark FROM user WHERE email = '%s'" % (email)
        db = connection()
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
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

    def reply(self,article_disscuss_id,article_number,respone_type,respone_user_id,disscuss,respone_user_ip,board_name):
        sql = \
        "INSERT INTO reply_from_pttLite(\
            article_disscuss_id,\
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
            article_disscuss_id,
            article_number,
            respone_type,
            respone_user_id,
            disscuss,
            respone_user_ip,
            board_name
        )
        db = connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
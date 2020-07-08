from datetime import datetime, timedelta
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from api import connection

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
        currsor.execute(sql)
        return cursor.fetchone()

    @staticmethod
    def get_user_list(username):
        sql = "SELECT nickname FROM user" % (username)
        db = connection()
        cursor = db.cursor()
        currsor.execute(sql)
        return cursor.fetchone()

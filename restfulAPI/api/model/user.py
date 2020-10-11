from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from api import InintAPP
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,decode_token,get_raw_jwt
)
from flask_mail import Message
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
import os
import base64
from os import listdir

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

class UserModel(InintAPP):
    def set_password(self,password):
        return generate_password_hash(password)

    def vaildate_password(self,email,password):
        sql = "SELECT pw_hash FROM users WHERE email = '{}'".format(email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        password_hash = cursor.fetchone()['pw_hash']
        db.commit()
        cursor.close()
        if password_hash:
            return check_password_hash(password_hash,password)
        else:
            return False

    @staticmethod
    def get_by_username(username):
        sql = "SELECT * FROM users WHERE nickname = '{}'".format(username)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            return user

    @staticmethod
    def get_by_id(username):
        sql = "SELECT nickname FROM users WHERE nickname = '{}'".format(username)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        db.commit()
        cursor.close()
        return res

    @staticmethod
    def get_user_list(username):
        sql = "SELECT nickname FROM user" % (username)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        db.commit()
        cursor.close()
        return res

    def follow_board(self,email,board_name):
        sql = "INSERT INTO following_boards(id,board_name,create_time) VALUES( (SELECT id FROM users WHERE email ='{}'),'{}',NOW() )".format( email,board_name )
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        return True

    def follow_article(self,email,board_name,article_number):
        article_url = "/" + board_name + "/" + article_number
        sql = "INSERT INTO following_articles(id,article_url,board_name,article_number,create_time)\
             VALUES( (SELECT id FROM users WHERE email ='{}'),'{}','{}','{}',NOW() )".format( email,article_url,board_name,article_number )
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        cursor.close()
        return True

    def get_following_boards(self,email):
        sql = "SELECT board_name,create_time FROM following_boards WHERE id = (SELECT id FROM users WHERE email ='{}')".format(email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()[0]
        db.close()
        cursor.close()
        return res

    def get_following_articles(self,email):
        sql = "SELECT article_url,create_time FROM following_articles WHERE id = (SELECT id FROM users WHERE email ='{}')".format(email)
        print(email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        db.close()
        cursor.close()
        return res
    
    def discuss(self,article_number,respone_type,respone_user_id,discussion,respone_user_ip,board_name):
        sql = \
        "INSERT INTO article_discussions(\
            from_pttLite, \
            article_number,\
            respone_type,\
            respone_user_id,\
            discussion,\
            respone_user_ip,\
            create_time,\
            last_update,\
            board_name\
            )\
        VALUES(true,'{},'{}','{}','{}','{}',NOW(),NOW(),'{}')".format(
            article_number,
            respone_type,
            respone_user_id,
            discussion,
            respone_user_ip,
            board_name
        )
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        cursor.close()

    def reply(self,article_discussion_id,article_number,respone_type,respone_user_id,discussion,respone_user_ip,board_name):
        sql = \
        "INSERT INTO reply_from_pttLite(\
            article_discussion_id,\
            article_number,\
            respone_type,\
            respone_user_id,\
            discussion,\
            respone_user_ip,\
            create_time,\
            last_update,\
            board_name\
            )\
        VALUES({},'{}','{}','{}','{}','{}',now(),now(),'{}')".format(
            article_discussion_id,
            article_number,
            respone_type,
            respone_user_id,
            discussion,
            respone_user_ip,
            board_name
        )
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        cursor.close()
    
    def forgot_password(self,email):
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE email = '%s'" % (email)
        cursor.execute(sql)
        if cursor.fetchone():
            access_token = create_access_token(identity=email)
            msg_title = 'PTT Lite 重設密碼'
            msg_sender = 'kiwichen.dev@gmail.com'
            msg_recipients = [str(email)]
            #msg_body = "密碼重設連結:{}".format("https://pttlite.cloudns.asia/resetpassword/" + str(access_token) )
            msg_html = '<a href="{}" >點我重設密碼</a>'.format("https://pttlite.ddns.net/resetpassword/" + str(access_token) )
            msg = Message(msg_title,
                        sender=msg_sender,
                        recipients=msg_recipients)
            #msg.body = msg_body
            msg.html = msg_html
            self.mail.send(msg)
            db.close()
            cursor.close()
            return True
        else:
            db.close()
            cursor.close()
            return False
    
    def vaildate_token(self,token):
        email = decode_token(token)['identity']
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE email = '{}' ".format(email)
        cursor.execute(sql)
        if cursor.fetchone():
            db.close()
            cursor.close()
            return True,email
        else:
            db.close()
            cursor.close()
            return False
    
    def reset_password(self,token):
        if self.vaildate_token(token)[0]:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'password', type = min_length_str(8), required=True,
                help='password require and length >= 8'
            )
            data = parser.parse_args()
            email = self.vaildate_token(token)[1]
            password = data['password']
            password_hash = self.set_password(password)
            db = self.connection()
            cursor = db.cursor()
            sql = "UPDATE users SET pw = '{}', pw_hash = '{}' WHERE email = '{}'".format(password,password_hash,email)
            cursor.execute(sql)
            db.commit()
            db.close()
            cursor.close()
            return True
        else:
            db.close()
            cursor.close()
            return False

    def refresh_token(self,email):
        token = {
            'access_token': create_access_token(identity=email)
        }
        return token

    def isUser(self,email):
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE email = '{}'".format(email)
        cursor.execute(sql)
        res = cursor.fetchone()
        db.close()
        cursor.close()   
        if res:
            return True
        else:
            return False
    
    def uploadFiles(self,email):
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT uuid FROM users WHERE email = '{}'".format(email)
        cursor.execute(sql)
        uuid = cursor.fetchone()['uuid']
        parser = reqparse.RequestParser()
        parser.add_argument('userIcon', type=FileStorage,location='files',help="userIcon is wrong.")
        img_file = parser.parse_args().get('userIcon')
        is_img = self.is_allowed_file(img_file)
        if img_file and is_img[0]:
            dirname = 'imgs/{}/icon'.format(uuid)
            os.makedirs(dirname,mode=0o777,exist_ok=True)
            save_path = os.path.join(dirname,'icon.'+ is_img[1] )
            img_file.save(save_path)
            del img_file
            del is_img
            return True
        else:
            del img_file
            del is_img
            return False

    def is_allowed_file(self,uploadFile):
        if '.' in uploadFile.filename:
            ext = uploadFile.filename.rsplit('.', 1)[1].lower()
            if ext in {'png','jpg', 'jpeg'}:
                del uploadFile
                return True,ext
            else:
                del uploadFile
                return False,ext
        else:
            del uploadFile
            return False

    def member_data(self,email):
        sql = "SELECT nickname FROM users WHERE email = '{}'".format(email)
        db = self.connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        user_data = dict()
        user_data['nickname'] = cursor.fetchone()['nickname']
        icon_path = 'imgs/{}/icon/'.format(email)

        try:
            files = listdir(icon_path)
        except:
            db.close()
            cursor.close()
            return user_data

        for f in files:
            if ('.' in f) and ( f.rsplit('.', 1)[1].lower() in {'jpg','png','jpeg'} ):
                icon_path = icon_path + str(f)
                print(icon_path)
                with open(r'{}'.format(icon_path), 'rb') as icon_path:
                    user_icon = base64.b64encode(icon_path.read())
                    user_data['user_icon'] = str(user_icon)
                    db.close()
                    cursor.close()
                    return user_data

        db.close()
        cursor.close()
        return user_data
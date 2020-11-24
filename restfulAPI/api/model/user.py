from datetime import datetime, timedelta
from flask import Response
from werkzeug.security import generate_password_hash, check_password_hash
from api import InitAPP
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
from api.model.boardArticle import LinkValidate
from api import mail

class UserModel(LinkValidate):
    def min_length_str(self,min_length):
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

    def set_password(self,password):
        return generate_password_hash(password)

    def validate_password(self,email,password):
        sql = "SELECT pw_hash,user_uuid FROM Users WHERE email = '{}'".format(email)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        password_hash = res['pw_hash']
        uuid = res['user_uuid']
        connection.close()
        if check_password_hash(password_hash,password):
            self.mysql_respon['respon_code'] = self.valid
            self.mysql_respon['respon_content'] = uuid
            return self.mysql_respon
        else:
            self.mysql_respon['respon_code'] = self.invalid
            return self.mysql_respon

    def get_user_data(self,email):
        sql = "SELECT * FROM Users WHERE email = '{}'".format(email)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.commit()
        connection.close()
        return res

    def get_user_by_uuid(self,uuid):
        sql = "SELECT * FROM Users WHERE user_uuid = '{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.commit()
        connection.close()
        return res

    def follow(self,*args):
        if len(args) == int(2):
            uuid = args[0]
            board_name = args[1]
            res = self.is_link(board_name)
            if res['respon_code'] == self.resource_found:
                sql = "SELECT * FROM FollowingBoards WHERE user_uuid='{}' AND board_name ='{}'".format(uuid,board_name)
                connection = self.connection()
                cursor = connection.cursor()
                cursor.execute(sql)
                if cursor.fetchone():
                    res['sql'] = "DELETE FROM FollowingBoards WHERE user_uuid='{}'AND board_name ='{}'".format(uuid,board_name)
                    self.db_commit_rollback(res)
                    res['respon_code'] = self.delete_success
                    return res
                else:
                    res['sql'] = sql = "INSERT INTO FollowingBoards(user_uuid,board_name,create_time) VALUES('{}','{}',now())".format(uuid,board_name)
                    self.db_commit_rollback(res)
                    res['respon_code'] = self.post_success
                    return res
            else:
                res
        elif len(args) == int(3):
            uuid = args[0]
            board_name = args[1]
            article_number = args[2]
            res = self.is_link(board_name,article_number)
            article_url = "/{}/{}".format(board_name,article_number)
            if res['respon_code'] == self.resource_found:
                sql = "SELECT * FROM FollowingArticles WHERE user_uuid='{}' AND article_url ='{}'".format(uuid,article_url)
                connection = self.connection()
                cursor = connection.cursor()
                cursor.execute(sql)
                if cursor.fetchone():
                    res['sql'] = "DELETE FROM FollowingArticles WHERE user_uuid='{}' AND article_url ='{}'".format(uuid,article_url)
                    self.db_commit_rollback(res)
                    res['respon_code'] = self.delete_success
                    return res
                else:
                    res['sql'] = "INSERT INTO FollowingArticles(user_uuid,article_url,board_name,article_number,create_time) VALUES('{}','{}','{}','{}',now())".format(uuid,article_url,board_name,article_number)
                    self.db_commit_rollback(res)
                    res['respon_code'] = self.post_success
                    return res
            else:
                return res
        else:
            res['respon_code'] = self.resource_not_found
            return res

    def unfollow(self,*args):
        if len(args) == int(2):
            uuid = args[0]
            board_name = args[1]
            res = self.is_link(args[1])
            if res['respon_code'] == self.resource_found:
                res['sql'] = "DELETE FROM FollowingBoards WHERE user_uuid='{}'AND board_name ='{}'".format(uuid,board_name)
                self.db_commit_rollback(res)
                res['respon_code'] = self.delete_success
                return res
            else:
                res
        elif len(args) == int(3):
            uuid = args[0]
            board_name = args[1]
            article_number = args[2]
            res = self.is_link(board_name,article_number)
            article_url = "/{}/{}".format(board_name,article_number)

            if res['respon_code'] == self.resource_found:
                res['sql'] = "DELETE FROM FollowingArticles WHERE user_uuid='{}' AND article_url ='{}'".format(args[0],article_url)
                self.db_commit_rollback(res)
                res['respon_code'] = self.delete_success
                return res
            else:
                return res
        else:
            res['respon_code'] = self.resource_not_found
            return res

    def get_following_boards(self,uuid):
        sql = "SELECT * FROM FollowingBoards WHERE user_uuid = '{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        following_boards = cursor.fetchall()
        connection.close()
        return following_boards

    def get_following_articles(self,uuid):
        sql = "SELECT * FROM FollowingArticles WHERE user_uuid = '{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        following_articles = cursor.fetchall()
        connection.close()
        return following_articles

    def discuss_or_reply(self,*args):
        if len(args) == int(6):
                sql = \
                "INSERT INTO ArticleDiscussions(\
                    from_pttLite,\
                    board_name,\
                    article_number,\
                    respone_type,\
                    respone_user_id,\
                    discussion,\
                    respone_user_ip,\
                    create_time,\
                    last_update\
                    )\
                VALUES(true,'{}','{}','{}','{}','{}','{}',NOW(),NOW())".format(
                    args[0],
                    args[1],
                    args[2],
                    args[3],
                    args[4],
                    args[5]
                )
                res = self.is_link(args[0],args[1])
                res['sql'] = sql
        elif len(args) == int(7):
                sql = \
                "INSERT INTO ReplyFromPttLite(\
                    articleDiscussions_nu,\
                    board_name,\
                    article_number,\
                    respone_type,\
                    respone_user_id,\
                    reply,\
                    respone_user_ip,\
                    create_time,\
                    last_update\
                    )\
                VALUES({},'{}','{}','{}','{}','{}','{}',NOW(),NOW())".format(
                    args[0],
                    args[1],
                    args[2],
                    args[3],
                    args[4],
                    args[5],
                    args[6]
                )
                res = self.is_link(args[0],args[1],args[2])
                res['sql'] = sql

        return self.db_commit_rollback(res)

    def forgot_password(self,email):
        try:
            sql = "SELECT user_uuid FROM Users WHERE email = '{}'".format(email)
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            uuid = cursor.fetchone()['user_uuid']
            isSucess = True
        except Exception as e:
            isSucess = False
            print(e)
            try:
                connection.rollback()
                connection.close()
            except Exception as e:
                print(e)
                return isSucess
        else:
            connection.close()
            if uuid:
                access_token = create_access_token(identity=uuid)
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
                mail.send(msg)
                return True
            else:
                return False
    
    def vaildate_token(self,token):
        uuid = decode_token(token)['identity']
        connection = self.connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM Users WHERE user_uuid = '{}' ".format(uuid)
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.close()
        if res:
            return True,uuid
        else:
            return False
    
    def reset_password(self,token):
        vaild = self.vaildate_token(token)
        if vaild[0]:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'password', type = self.min_length_str(8), required=True,
                help='password require and length >= 8'
            )
            data = parser.parse_args()
            password = data['password']
            password_hash = self.set_password(password)
            uuid = vaild[1]
            try:
                sql = "UPDATE Users SET pw = '{}', pw_hash = '{}' WHERE user_uuid = '{}'".format(password,password_hash,uuid)
                connection = self.connection()
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                isSucess = True
            except Exception as e:
                isSucess = False
                print(e)
                connection.rollback()
            else:
                connection.close()
            finally:
                return isSucess
        else:
            return False

    def change_password(self,uuid,password):
        password_hash = self.set_password(password)
        try:
            sql = "UPDATE Users SET pw = '{}', pw_hash = '{}' WHERE user_uuid = '{}'".format(password,password_hash,uuid)
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            isSucess = True
        except Exception as e:
            isSucess = False
            print(e)
            connection.rollback()
        else:
            connection.close()
        finally:
            return isSucess

    def refresh_token(self,uuid):
        token = {
            'access_token': create_access_token(identity=uuid)
        }
        return token

    def isUser(self,email):
        connection = self.connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "SELECT * FROM Users WHERE email = '{}'".format(email)
                cursor.execute(sql)
                res = cursor.fetchone()
                connection.close()
            except:
                connection.rollback()
                self.mysql_respon['respon_code'] = self.mysql_error
                return self.mysql_respon
            else:
                if res:
                    self.mysql_respon['respon_code'] = self.resource_found
                    return self.mysql_respon
                else:
                    self.mysql_respon['respon_code'] = self.resource_not_found
                    return self.mysql_respon
        else:
            self.mysql_respon['respon_code'] = self.mysql_offline
            return self.mysql_respon
    
    def uploadFiles(self,uuid):
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
    
    def upload_images(self,img_file):
        pass

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
    
    def my_reply(self,uuid):
        sql = "SELECT * FROM ReplyFromPttLite WHERE respone_user_id = ( SELECT nickname FROM Users WHERE user_uuid = '{}' )".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        connection.close()
        return res

    def my_discussions(self,uuid):
        sql = "SELECT * FROM ArticleDiscussions WHERE respone_user_id = ( SELECT nickname FROM Users WHERE user_uuid = '{}' )".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        connection.close()
        return res

    def login_records(self,uuid):
        sql = "INSERT INTO LoginRecords(user_uuid,login_time,ip) VALUES('{}',now(),'111.111.111.111')".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

    def get_login_records(self,uuid):
        sql = "SELECT login_time,ip FROM LoginRecords WHERE user_uuid = '{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        connection.close()
        return res

    def member_data(self,uuid):
        user_data = dict()
        # user_data['following_boards'] = self.get_following_boards(uuid)
        # user_data['following_articles'] = self.get_following_articles(uuid)
        # user_data['my_reply'] = self.my_reply(uuid)
        # user_data['my_discussions'] = self.my_discussions(uuid)
        user_data['login_records'] = self.get_login_records(uuid)
        sql = "SELECT nickname,email FROM Users WHERE user_uuid = '{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        res = cursor.fetchone()
        user_data['nickname'] = res['nickname']
        user_data['email'] = res['email']
        user_data['user_icon'] = None
        icon_path = 'imgs/{}/icon/'.format(uuid)
        try:
            files = listdir(icon_path)
        except:
            connection.close()
            return user_data
        for f in files:
            if ('.' in f) and (f.rsplit('.',1)[1].lower() in {'jpg','png','jpeg'}):
                icon_path = icon_path + str(f)
                print(icon_path)
                with open(r'{}'.format(icon_path), 'rb') as icon_path:
                    # user_icon = base64.b64encode(icon_path.read())
                    # user_data['user_icon'] = str(user_icon)
                    user_data['user_icon'] = str(icon_path)
                    connection.close()
                    return user_data
        connection.close()
        return user_data
        
    def user_privileges(self,uuid):
        sql = "SELECT user_privileges FROM Users WHERE user_uuid ='{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchone()['user_privileges']
        
    def user_images(self,uuid,albums,image_name):
        if albums == 'icon':
            icon_path = 'imgs/{}/icon/'.format(uuid)
            try:
                files = listdir(icon_path)
            except:
                return
            for f in files:
                if ('.' in f) and (f.split('.',1)[1].lower() in {'jpg','jpeg','jpeg'}):
                    print(icon_path)
                    with open (r'{}'.format(icon_path),'rb') as icon_path:
                        return str(icon_path)
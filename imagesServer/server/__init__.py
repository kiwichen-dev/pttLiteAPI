from flask import Flask,Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import pymysql.cursors
import os
from os import listdir
from server.config import Config

# def imgs(uuid,albums='icon',image_name):
    # if albums = 'icon':
    #     icon_path = 'static/{}/icon/'.format(uuid)
    #     try:
    #         files = listdir(icon_path)
    #     except:
    #         return None
    #     for f in files:
    #         if ('.' in f) and (f.split('.',1)[1].lower() in {'jpg','jpeg','jpeg'}):
    #             print(icon_path)
    #             with open (r'{}'.format(icon_path),'rb') as icon_path:
    #                 return str(icon_path)
    # pass

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
jwt = JWTManager(app)
CORS(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

class InitAPP():
    def __init__(self):
        self.mysql_offline = int(0)
        self.mysql_is_working = int(1)
        self.mysql_error = int(2)
        self.resource_found = int(3)
        self.resource_not_found = int(4)
        self.post_success = int(5)
        self.put_success = int(6)
        self.delete_success = int(7)
        self.valid = int(8)
        self.invalid = int(9)
        self.mysql_respon = dict()
        self.mysql_respon['respon_code'] = None
        self.mysql_respon['respon_content'] = None
        self.mysql_respon['sql'] = None
    
    @staticmethod
    def connection():
        connection = pymysql.connect(
        host="192.168.31.194",
        port=int(3306),
        user="flask",
        password="quQ351dTx",
        db="PTTLite",
        max_allowed_packet="16M",
        cursorclass=pymysql.cursors.DictCursor
        )
        return connection

from server.resource.upload import Images,Upload_images

def create_app():
    api.add_resource(Images,'/images/<img_file>')
    api.add_resource(Upload_images,'/upload_images')
    return app
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

from server.model.upload import Upload_images

def create_app():
    api.add_resource(Upload_images,'/upload_images/<img_file>')
    return app
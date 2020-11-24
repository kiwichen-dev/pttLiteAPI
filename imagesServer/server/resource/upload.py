from flask import Response,jsonify
from flask_restful import reqparse,Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from server import InitAPP
from server.model.upload import Upload
from werkzeug.datastructures import FileStorage

class ViewImages(InitAPP,Resource):
    def get(self,img_file):
        with open(r'static/{}'.format(img_file), 'rb') as f:
            print('開啟圖片static/{}'.format(img_file))
            image = f.read()
            resp = Response(image, mimetype="image/png")
            return resp

class FrontendImages(InitAPP,Resource):
    def get(self,folder_name,img_file):
        try:
            with open(r'static/frontend/{}/{}'.format(folder_name,img_file), 'rb') as f:
                print('static/frontend/{}/{}'.format(folder_name,img_file))
                image = f.read()
                resp = Response(image, mimetype="image/png")
                return resp
        except:
            return {'msg':'not found'},404

class Upload_images(Upload,Resource):
    @jwt_required
    def post(self):
        uuid = get_jwt_identity()
        sql = "SELECT * FROM Users WHERE user_uuid = '{}'".format(uuid)
        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.fetchone():
            connection.close()
            parser = reqparse.RequestParser()
            parser.add_argument('images',type=FileStorage,location='files',help="jpg jpeg png only",action="append")
            arg = parser.parse_args()
            img_files = arg['images']
            is_upload,img_list = self.uploadFiles(img_files)
            return jsonify(img_list)
from flask import Response
from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

class Upload_images(Resource):
    @jwt_required
    def get(self,img_file):
        uuid = get_jwt_identity()
        print(uuid)
        with open(r'static/{}'.format(img_file), 'rb') as f:
            print('static/{}'.format(img_file))
            image = f.read()
            resp = Response(image, mimetype="image/png")
            return resp

    @jwt_required
    def post(self,img_file):
        with open(r'static/{}'.format(img_file), 'rb') as f:
            print('static/{}'.format(img_file))
            image = f.read()
            resp = Response(image, mimetype="image/png")
            return resp
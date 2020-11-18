import os
from datetime import timedelta

class Config():
    #JWT - General Options:
    JWT_SECRET_KEY = 'fk6hcej67az355szr'
    JWT_TOKEN_LOCATION = ['headers', 'query_string']
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = int(900)
    JWT_REFRESH_TOKEN_EXPIRES = int(86400)*int(30)
    JWT_ALGORITHM = 'HS256'

    #JWT - Header Options
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # JTW - Json Body Options
    JWT_JSON_KEY = 'access_token'
    JWT_REFRESH_JSON_KEY = 'refresh_token'

    #JWT - Logout
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SECRET_KEY = 'development'
    UPLOAD_FOLDER = './images'
    ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
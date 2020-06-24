from datetime import datetime
from hashlib import md5
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from api import db,login_manager

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    nickname = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(30))
    password_hash = db.Column(db.String(300))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_modify_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'id={},email={}, nickname={}, password_hash={}, create_time={}, last_modify_time={}'.format(
                self.id,self.email, self.nickname, self.password_hash, self.create_time, self.last_modify_time)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    """
    def get_jwt(self, expire=7200):
        return jwt.encode(
            {
                'email': self.email,
                'exp': time.time() + expire
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')
    """
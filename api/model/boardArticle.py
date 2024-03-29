from datetime import datetime
import time
from flask import current_app
from api import db

class Category(db.Model):
    __tablename__ = 'category'
    board_link = db.Column(db.String(150), primary_key=True)
    board_name = db.Column(db.String(30), unique=True)
    board_nuse = db.Column(db.String(10))
    board_class = db.Column(db.String(15))
    board_title = db.Column(db.String(80))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'board_link={}, board_name={}, board_nuse={}, board_class={}, board_title={}, last_update={}'.format(
                self.board_link, self.board_name, self.board_nuse, self.board_class, self.board_title, self.last_update)

class Article(db.Model):
    __tablename__ = 'article'
    article_url = db.Column(db.String(150), primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(30))
    author_ip = db.Column(db.String(100))
    body = db.Column(db.Text)
    push_count = db.Column(db.String(10))
    create_time = db.Column(db.String(20))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    board_link = db.Column(db.String(150), db.ForeignKey('category.board_link'))

    def __repr__(self):
        return 'article_url={}, title={}, author={}, author_ip, body={}, push_count={}, create_time={}, last_update={},board_link={}'.format(
                self.article_url, self.title, self.author, self.author_ip, self.body, self.push_count, self.create_time, self.last_update, self.board_link)

"""
class Article_content(db.Model):
    __tablename__ = 'article_content'
    article_url = db.Column(db.String(300),primary_key=True)
    body = db.Column(db.Text, db.ForeignKey('article.body'))
    author_ip = db.Column(db.String(100))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return 'article_url={}, article_body={}, author_ip={}, last_update={}'.format(
                self.article_url, self.article_body, self.author_ip, self.last_update)
"""

class Article_disscuss(db.Model):
    __tablename__ = 'article_disscuss'
    article_url = db.Column(db.String(300),primary_key=True)
    disscuss_user_id = db.Column(db.String(15))
    disscuss = db.Column(db.String(500))
    respone_user_ip = db.Column(db.String(100))
    create_time = db.Column(db.String(15))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'article_url={}, disscuss_respon={}, disscuss_user_id={}, disscuss={}, respone_user_ip={}, create_time={}, last_update={}'.format(
                self.article_url, self.disscuss_respon, self.disscuss_user_id, self.disscuss, self.respone_user_ip, self.create_time, self.last_update)

class Pushcount():
    def __init__(self):
        self.__good = list()
        self.__neutral = list()
        self.__bad = list()
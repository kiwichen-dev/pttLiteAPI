from datetime import datetime
import time
from flask import current_app
from api import InintAPP

"""
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

class Article_content(db.Model):
    __tablename__ = 'article_content'
    article_url = db.Column(db.String(300),primary_key=True)
    body = db.Column(db.Text, db.ForeignKey('article.body'))
    author_ip = db.Column(db.String(100))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return 'article_url={}, article_body={}, author_ip={}, last_update={}'.format(
                self.article_url, self.article_body, self.author_ip, self.last_update)


class Article_discuss(db.Model):
    __tablename__ = 'article_discuss'
    article_url = db.Column(db.String(300),primary_key=True)
    discuss_user_id = db.Column(db.String(15))
    discuss = db.Column(db.String(500))
    respone_user_ip = db.Column(db.String(100))
    create_time = db.Column(db.String(15))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'article_url={}, discuss_respon={}, discuss_user_id={}, discuss={}, respone_user_ip={}, create_time={}, last_update={}'.format(
                self.article_url, self.discuss_respon, self.discuss_user_id, self.discuss, self.respone_user_ip, self.create_time, self.last_update)
"""

class Pushcount():
    def __init__(self):
        self.__good = list()
        self.__neutral = list()
        self.__bad = list()

class LinkVaildate(InintAPP):
    def check_Discussion(self,board,article):
        sql = "SELECT * FROM article WHERE board_name = '%s' AND article_number = '%s'" % (board,article)
        pymysql = self.connection()
        cursor = pymysql.cursor()
        cursor.execute(sql)
        if cursor.fetchone():
            return True
        else:
            return False

    def check_Reply(self,board,article,discussion_id):
        sql = "SELECT * FROM article_discuss WHERE board_name = '%s' AND article_number = '%s' AND discussion_id ='%s'" % (board,article,discussion_id)
        pymysql = self.connection()
        cursor = pymysql.cursor()
        cursor.execute(sql)
        if cursor.fetchone():
            return True
        else:
            return False
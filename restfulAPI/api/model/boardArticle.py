from datetime import datetime
import time
from flask import current_app
from api import InitAPP,pool

"""
class Category(connection.Model):
    __tablename__ = 'category'
    board_link = connection.Column(connection.String(150), primary_key=True)
    board_name = connection.Column(connection.String(30), unique=True)
    board_nuse = connection.Column(connection.String(10))
    board_class = connection.Column(connection.String(15))
    board_title = connection.Column(connection.String(80))
    last_update = connection.Column(connection.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'board_link={}, board_name={}, board_nuse={}, board_class={}, board_title={}, last_update={}'.format(
                self.board_link, self.board_name, self.board_nuse, self.board_class, self.board_title, self.last_update)

class Article(connection.Model):
    __tablename__ = 'article'
    article_url = connection.Column(connection.String(150), primary_key=True)
    title = connection.Column(connection.String(255))
    author = connection.Column(connection.String(30))
    author_ip = connection.Column(connection.String(100))
    body = connection.Column(connection.Text)
    push_count = connection.Column(connection.String(10))
    create_time = connection.Column(connection.String(20))
    last_update = connection.Column(connection.DateTime, default=datetime.utcnow)
    board_link = connection.Column(connection.String(150), connection.ForeignKey('category.board_link'))

    def __repr__(self):
        return 'article_url={}, title={}, author={}, author_ip, body={}, push_count={}, create_time={}, last_update={},board_link={}'.format(
                self.article_url, self.title, self.author, self.author_ip, self.body, self.push_count, self.create_time, self.last_update, self.board_link)

class Article_content(connection.Model):
    __tablename__ = 'article_content'
    article_url = connection.Column(connection.String(300),primary_key=True)
    body = connection.Column(connection.Text, connection.ForeignKey('article.body'))
    author_ip = connection.Column(connection.String(100))
    last_update = connection.Column(connection.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return 'article_url={}, article_body={}, author_ip={}, last_update={}'.format(
                self.article_url, self.article_body, self.author_ip, self.last_update)


class Article_discuss(connection.Model):
    __tablename__ = 'article_discuss'
    article_url = connection.Column(connection.String(300),primary_key=True)
    discuss_user_id = connection.Column(connection.String(15))
    discuss = connection.Column(connection.String(500))
    respone_user_ip = connection.Column(connection.String(100))
    create_time = connection.Column(connection.String(15))
    last_update = connection.Column(connection.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'article_url={}, discuss_respon={}, discuss_user_id={}, discuss={}, respone_user_ip={}, create_time={}, last_update={}'.format(
                self.article_url, self.discuss_respon, self.discuss_user_id, self.discuss, self.respone_user_ip, self.create_time, self.last_update)
"""

class Pushcount():
    def __init__(self):
        self.__good = list()
        self.__neutral = list()
        self.__bad = list()

class LinkValidate(InitAPP):
    def is_link(self,*args):
        if len(args) == int(1):
            sql = "SELECT * FROM Category WHERE board_name = '{}'".format(args[0])
        elif len(args) == int(2):
            sql = "SELECT * FROM Articles WHERE board_name = '{}' AND article_number = '{}'".format(args[0],args[1])
        elif len(args) == int(3):
            sql = "SELECT * FROM ArticleDiscussions WHERE nu = '{}' AND board_name = '{}' AND article_number = '{}'".format(args[0],args[1],args[2])
        else:
            return self.mysql_error
        # pool = self.pool()
        connection = pool.get_conn()
        if connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            # connection.close()
            # cursor.close()
            pool.release(connection)
            if res:
                self.mysql_respon['respon_code'] = self.request_sucess
                self.mysql_respon['respon_content'] = res
                return self.mysql_respon
            else:
                self.mysql_respon['respon_code'] = self.request_not_found
                return self.mysql_respon
        else:
            return self.mysql_offline

    # def vaildate_board(self,board_name):
    #     connection = InitAPP.connection()
    #     if connection:
    #         sql = "SELECT * FROM Category WHERE board_name = '{}'".format(board_name)
    #         cursor = connection.cursor()
    #         cursor.execute(sql)
    #         res = cursor.fetchone()
    #         connection.close()
    #         cursor.close()
    #         if res:
    #             self.mysql_respon['respon_code'] = self.request_sucess
    #             self.mysql_respon['respon_content'] = res
    #             return self.mysql_respon
    #         else:
    #             self.mysql_respon['respon_code'] = self.request_not_found
    #             return self.mysql_respon
    #     else:
    #         return self.__mysql_respon

    # def vaildate_article(self,board_name,article_number):
    #     connection = InitAPP.connection()
    #     if connection:
    #         sql = "SELECT * FROM Articles WHERE board_name = '{}' AND article_number = '{}'".format(board_name,article_number)
    #         cursor = connection.cursor()
    #         cursor.execute(sql)
    #         res = cursor.fetchone()
    #         connection.close()
    #         cursor.close()
    #         if res:
    #             self.mysql_respon['respon_code'] = self.request_sucess
    #             self.mysql_respon['respon_content'] = res
    #             return self.mysql_respon
    #         else:
    #             self.mysql_respon['respon_code'] = self.request_not_found
    #             return self.mysql_respon
    #     else:
    #         return self.__mysql_respon

    # def vaildate_discussion(self,nu,board_name,article_number):
    #     connection = InitAPP.connection()
    #     if connection:
    #         sql = "SELECT * FROM ArticleDiscussions WHERE nu = '{}' AND board_name = '{}' AND article_number = '{}'".format(nu,board_name,article_number)
    #         cursor = connection.cursor()
    #         cursor.execute(sql)
    #         res = cursor.fetchone()
    #         connection.close()
    #         cursor.close()
    #         if res:
    #             self.mysql_respon['respon_code'] = self.request_sucess
    #             self.mysql_respon['respon_content'] = res
    #             return self.mysql_respon
    #         else:
    #             self.mysql_respon['respon_code'] = self.request_not_found
    #             return self.mysql_respon
    #     else:
    #         return self.__mysql_respon
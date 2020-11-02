from flask import jsonify, request, current_app
from api import InitAPP
from api.model.boardArticle import LinkValidate
from flask_restful import Resource, reqparse
import re
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from api.model.user import UserModel

class Index(UserModel,Resource):
    @jwt_required 
    def get(self):
        index = dict()
        connection = self.connection()
        cursor = connection.cursor()
        sql = 'SELECT * FROM IndexArticles'
        cursor.execute(sql)
        index_articles = cursor.fetchall()  
        sql = "SELECT * FROM Top8AmountOfLikesBoards ORDER BY amount_of_likes DESC LIMIT 8"
        cursor.execute(sql)
        index['top_8_amount_of_likes_boards'] = cursor.fetchall()
        # uuid = get_jwt_identity()[0]
        uuid = get_jwt_identity()
        following_articles = list()
        index_articles_add_is_following = list()
        for _ in self.get_following_articles(uuid):
            following_articles.append(_['article_number'])
        for _ in index_articles:
            if _['article_number'] in following_articles:
                _['is_following'] = True
                index_articles_add_is_following.append(_)
            else:
                _['is_following'] = False
                index_articles_add_is_following.append(_)
        index['articles'] = index_articles_add_is_following
        connection.close()
        return jsonify(index)

class Board(LinkValidate, Resource):
    @jwt_required 
    def get(self, board_name, order_by='create_time', limit='100'):
        res = self.is_link(board_name)
        if res['respon_code'] == self.resource_found:
            connection = self.connection()
            limit = int(limit)
            if limit <= int(0):
                return {'msg':'can not quire 0 article'},404
            elif limit == int(100):
                sql = "SELECT * FROM DescCreateArticles WHERE board_name ='{}'".format(board_name)
                cursor = connection.cursor()
                cursor.execute(sql)
                articles = dict()
                articles['board'] = cursor.fetchall()
                connection.close()
                return jsonify(articles)
            else:
                sql = "SELECT board_name,article_number,article_url,title,author,author_ip,ip_location,content_snapshot,\
                        amount_of_discussions,amount_of_likes,amount_of_neutrals,amount_of_dislikes,create_time \
                        FROM Articles WHERE board_name = '{}' ORDER BY {} DESC limit {}".format(board_name,order_by,limit)
                cursor = connection.cursor()
                cursor.execute(sql)
                articles = dict()
                articles['board'] = cursor.fetchall()
                connection.close()
                return jsonify(articles)
        elif res['respon_code'] == self.resource_not_found:
            return {'msg': 'Board not found'},404
        else:
            return {'msg':'Get an error'},500

class AllBoards(LinkValidate, Resource):
    @jwt_required 
    def get(self):
        connection = self.connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Category')
            category = cursor.fetchall()
            package = dict()
            package['all_boards'] = category
            connection.close()
            return jsonify(package)
        else:
            return {'msg':'MySQL offline'},500

class ArticlePage(UserModel, Resource):
    @jwt_required 
    def get(self, board_name, article_number):
        res = self.is_link(board_name,article_number)
        if res['respon_code'] == self.resource_found:
            connection = self.connection()
            if connection:
                cursor = connection.cursor()
                article_fetch = res['respon_content']
                sql = "SELECT nu,from_pttLite,respone_type,respone_user_id,discussion,respone_user_ip,create_time FROM ArticleDiscussions WHERE article_number ='{}'".format(article_number)
                cursor.execute(sql)
                article_discussions = cursor.fetchall()
                sql = "SELECT nu,respone_type,respone_user_id,reply,respone_user_ip,create_time,last_update FROM ReplyFromPttLite WHERE board_name ='{}' AND article_number ='{}'".format(board_name, article_number)
                cursor.execute(sql)
                reply_from_pttLite = cursor.fetchall()
                article = dict()
                # article_page = dict()
                article['board_name'] = article_fetch['board_name']
                article['article_number'] = article_fetch['article_number']
                article['article_url'] = article_fetch['article_url']
                article['title'] = article_fetch['title']
                article['author'] = article_fetch['author']
                article['ip_location'] = article_fetch['ip_location']
                article['content'] = article_fetch['content']
                article['amount_of_discussions'] = article_fetch['amount_of_discussions']
                article['amount_of_likes'] = article_fetch['amount_of_likes']
                article['amount_of_neutrals'] = article_fetch['amount_of_neutrals']
                article['amount_of_dislikes'] = article_fetch['amount_of_dislikes']
                article['create_time'] = article_fetch['create_time']
                article['last_update'] = article_fetch['last_update']
                article['discussions'] = article_discussions
                article['is_following'] = False
                article['reply_from_pttLite'] = reply_from_pttLite
                uuid = get_jwt_identity()
                for _ in self.get_following_articles(uuid):
                    if _['article_number'] == article['article_number']:
                        article['is_following'] = True
                # article_page['article_page'] = article
                connection.close()
                return jsonify(article)
            else:
                return {'msg':'MySQL offline'},500
        else:
            return self.analysis_return(res)

class Search(UserModel,Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'key_word', type=str, required=True, help='required key_word'
        )
        data = parser.parse_args()
        key_word = data['key_word']
        connection = self.connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM Articles WHERE title LIKE '{}'".format('%'+key_word+'%')
        cursor.execute(sql)
        searching_result = cursor.fetchall()
        connection.close()
        return jsonify(searching_result)
from flask import jsonify, request, current_app
from api import InintAPP
#from api.model.boardArticle import Category,Article,Article_discuss
from flask_restful import Resource, reqparse
import re


class Index(InintAPP, Resource):
    def get(self):
        index = dict()
        distinct_board_name_top = list()
        db = self.connection()
        if db:
            sql = "SELECT DISTINCT board_name FROM Category"
            cursor = db.cursor()
            cursor.execute(sql)
            distinct_board_name = cursor.fetchall()
            for board_name in distinct_board_name:
                sql = "SELECT * FROM Articles WHERE board_name = '{}' AND trim(content_snapshot)!='' ORDER BY amount_of_discussions DESC LIMIT 1".format(board_name['board_name'])
                cursor.execute(sql)
                res = cursor.fetchone()
                if res:
                    distinct_board_name_top.append(res)
            index['articles'] = distinct_board_name_top
            index['image'] = '/index.jpg'      
            sql = "SELECT * FROM Top8AmountOfLikesBoards ORDER BY amount_of_likes DESC LIMIT 8"
            cursor.execute(sql)
            top_8_amount_of_likes_boards = cursor.fetchall()
            index['top_8_amount_of_likes_boards'] = top_8_amount_of_likes_boards
            db.close()
            cursor.close()
            return jsonify(index)
        else:
            return {'msg':'MySQL offline'},500

class News(InintAPP, Resource):
    def get(self):
        pass

class Board(InintAPP, Resource):
    def get(self, board_name, order_by='create_time', limit='200'):
        db = self.connection()
        if db:
            sql = "SELECT * FROM Articles WHERE board_name = '{}' ORDER BY {} DESC limit {}".format(board_name, order_by, limit)
            cursor = db.cursor()
            cursor.execute(sql)
            package = dict()
            package['board'] = cursor.fetchall()
            db.close()
            cursor.close()
            return jsonify(package)
        else:
            return {'msg':'MySQL offline'},500

class AllBoards(InintAPP, Resource):
    def get(self):
        db = self.connection()
        if db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM Category')
            category = cursor.fetchall()
            cursor.close()
            package = dict()
            package['all_boards'] = category
            db.close()
            cursor.close()
            return jsonify(package)
        else:
            return {'msg':'API error'},500

class ArticlePage(InintAPP, Resource):
    def get(self, board_name, article_number):
        db = self.connection()
        if db:
            sql = "SELECT * FROM Articles WHERE board_name = '{}' AND article_number = '{}'".format(board_name, article_number)
            cursor = db.cursor()
            cursor.execute(sql)
            article_fetch = cursor.fetchall()[0]
            if article_fetch:
                sql = "SELECT nu,from_pttLite,respone_type,respone_user_id,discussion,respone_user_ip,create_time FROM ArticleDiscussions WHERE article_number ='{}'".format(article_number)
                cursor.execute(sql)
                article_discussions = cursor.fetchall()
                sql = "SELECT nu,respone_type,respone_user_id,reply,respone_user_ip,create_time,last_update FROM ReplyFromPttLite WHERE board_name ='{}' AND article_number ='{}'".format(board_name, article_number)
                cursor.execute(sql)
                reply_from_pttLite = cursor.fetchall()
                article = dict()
                article_page = dict()
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
                article['reply_from_pttLite'] = reply_from_pttLite
                article_page['article_page'] = article
                db.close()
                cursor.close()
                return jsonify(article_page)
            else:
                db.close()
                cursor.close()
                return {'msg': 'article not found'}, 404
        else:
            return {'msg':'MySQL offline'},500

def search():
    cursor = db.cursor()
    if request.method == 'POST':
        keyWord = request.form.get('keyWord')
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM Articles WHERE title LIKE '%s'" % (
            '%' + keyWord + '%')
        cursor.execute(sql)
        searchingResult = cursor.fetchall()
        db.close()
        cursor.close()
        return jsonify('search.html', searchingResult=searchingResult)

class BoardToList(InintAPP, Resource):
    def get(self):
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT DISTINCT board_name FROM Category ORDER BY board_name ASC"
        cursor.execute(sql)
        distinct_board_name = cursor.fetchall()
        board_to_list = dict()
        i = 0
        for d in distinct_board_name:
            board_to_list[str(d['board_name'])] = str(i)
            i += 1
        db.close()
        cursor.close()
        return jsonify(board_to_list)

class Article_Left_Join(InintAPP, Resource):
    def get(self, board, article_number):
        db = self.connection()
        cursor = db.cursor()
        sql = "SELECT * FROM Articles WHERE board_name = '%s' AND article_number = '%s'" % (
            board, article_number)
        cursor.execute(sql)
        if cursor.fetchone():
            sql = "SELECT * FROM Articles WHERE article_number = '%s'" % (
                article_number)
            cursor.execute(sql)
            article_content = cursor.fetchone()

            sql = "SELECT COUNT(*) FROM ArticleDiscussions WHERE article_number = '%s' and respone_type='推 '" % (
                article_number)
            cursor.execute(sql)
            like = cursor.fetchone()

            sql = "SELECT COUNT(*) FROM ArticleDiscussions WHERE article_number = '%s' and respone_type='→ '" % (
                article_number)
            cursor.execute(sql)
            neutral = cursor.fetchone()

            sql = "SELECT COUNT(*) FROM ArticleDiscussions WHERE article_number = '%s' and respone_type='噓 '" % (
                article_number)
            cursor.execute(sql)
            diskike = cursor.fetchone()

            sql = "SELECT * FROM ArticleDiscussions LEFT JOIN reply_from_pttLite ON article_discussions.discussion.id  = reply_from_pttLite.article_discussion_id WHERE ArticleDiscussions.article_number = '%s'" % (
                article_number)
            cursor.execute(sql)
            reply_from_pttLite = cursor.fetchall()

            article = dict()
            article['article_url'] = '/' + article_content['board_name'] + \
                '/' + article_content['article_number']
            article['board_name'] = article_content['board_name']
            article['article_number'] = article_content['article_number']
            article['title'] = article_content['title']
            article['author'] = article_content['author']
            article['author_ip'] = article_content['author_ip'].split(
                '(')[-1].replace(')', '')
            article['body'] = article_content['body']
            article['push_count'] = article_content['push_count']
            article['create_time'] = str(article_content['create_time'])
            article['discussions'] = reply_from_pttLite
            db.close()
            cursor.close()
            return jsonify(article)

        else:
            db.close()
            cursor.close()
            return {'message': 'article not found'}, 404

class ArticleContent(InintAPP,Resource):
    def get(self,board_name,article_number):
        db = self.connection()
        if db:
            sql = "SELECT content FROM Articles WHERE board_name = '{}' AND article_number = '{}'".format(board_name,article_number)
            cursor = db.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()['content']
            return jsonify(res)
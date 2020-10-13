from flask import jsonify, request, current_app
from api import InintAPP
#from api.model.boardArticle import Category,Article,Article_discuss
from flask_restful import Resource, reqparse
import re


class Index(InintAPP, Resource):
    def get(self):
        index = dict()
        distinct_board_name_top = list()
        try:
            sql = "SELECT DISTINCT board_name FROM Category"
            db = self.connection()
            cursor = db.cursor()
            cursor.execute(sql)
            distinct_board_name = cursor.fetchall()
        except Exception as e:
            print(e)
            db.rollback()
            db.close()
            cursor.close()
            return {'msg':'API error'},500  #掛了就不執行以下
        else:
            for board_name in distinct_board_name:
                try:
                    sql = "SELECT * FROM Articles WHERE board_name = '{}' AND trim(body)!='' ORDER BY discussion_count DESC LIMIT 1".format(
                        board_name['board_name'])
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    if res:
                        distinct_board_name_top.append(res)
                except Exception as e:
                    print(e)
                else:
                    pass
                finally:
                    pass
        finally:
            pass

        index['articles'] = distinct_board_name_top
        index['image'] = '/index.jpg'      
        try:
            sql = "SELECT * FROM Top8LikeCountBoards ORDER BY like_count DESC LIMIT 8"
            cursor.execute(sql)
            top_8_like_count_boards = cursor.fetchall()
            index['top_8_like_count_boards'] = top_8_like_count_boards
        except Exception as e:
            print(e)
            index['top_8_like_count_boards'] = None
            try:
                db.rollback()
                db.close()
                cursor.close()
            except Exception as e:
                print(e)
                pass #無法關閉 直接去finally
        else:
            db.close()
            cursor.close()
        finally: #有無top_8_like_count_boards都回傳資料
            return jsonify(index)

class News(InintAPP, Resource):
    def get(self):
        pass

class Board(InintAPP, Resource):
    def get(self, board_name, order_by='create_time', limit='200'):
        try:
            sql = "SELECT * FROM Articles WHERE board_name = '{}' ORDER BY {} DESC limit {}".format(board_name, order_by, limit)
            db = self.connection()
            cursor = db.cursor()
            cursor.execute(sql)
        except Exception as e:
            print(e)
            try: #出錯時 嘗試rollback或關閉連線
                db.rollback()
                db.close()
                ursor.close()
                return {'msg':'API error'},500
            except Exception as e:
                print(e)
                return {'msg':'API error'},500
        else: #無錯誤時執行
            package = dict()
            package['board'] = cursor.fetchall()
            db.close()
            cursor.close()
            return jsonify(package)

class AllBoards(InintAPP, Resource):
    def get(self):
        db = self.connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Category')
        category = cursor.fetchall()
        cursor.close()
        package = dict()
        package['all_boards'] = category
        db.close()
        cursor.close()
        return jsonify(package)

class ArticlePage(InintAPP, Resource):
    def get(self, board_name, article_number):
        try:
            sql = "SELECT * FROM Articles WHERE board_name = '{}' AND article_number = '{}'".format(board_name, article_number)
            db = self.connection()
            cursor = db.cursor()
            cursor.execute(sql)
            article_content = cursor.fetchall()[0]
        except Exception as e:
            print(e)
            try:
                db.rollback()
                db.close()
                ursor.close()
                return {'msg':'API error'},500
            except Exception as e:
                print(e)
                return {'msg':'API error'},500
            else:
                pass
            finally:
                pass

        if article_content:
            try:
                sql = "SELECT nu,from_pttLite,respone_type,respone_user_id,discussion,respone_user_ip,create_time FROM ArticleDiscussions WHERE article_number ='{}'".format(article_number)
                cursor.execute(sql)
                article_discussions = cursor.fetchall()
                sql = "SELECT nu,respone_type,respone_user_id,reply,respone_user_ip,create_time,last_update FROM ReplyFromPttLite WHERE board_name ='{}' AND article_number ='{}'".format(board_name, article_number)
                cursor.execute(sql)
                reply_from_pttLite = cursor.fetchall()
            except Exception as e:
                print(e)
                try:
                    db.rollback()
                    db.close()
                    ursor.close()
                    return {'msg':'API error'},500
                except Exception as e:
                    print(e)
                    return {'msg':'API error'},500
            else:
                article = dict()
                article_page = dict()
                article['board_name'] = article_content['board_name']
                article['article_number'] = article_content['article_number']
                article['article_url'] = article_content['article_url']
                article['title'] = article_content['title']
                article['author'] = article_content['author']
                article['ip_location'] = article_content['ip_location']
                article['body'] = article_content['body']
                article['discussion_count'] = article_content['discussion_count']
                article['like_count'] = article_content['like_count']
                article['neutral_count'] = article_content['neutral_count']
                article['dislike_count'] = article_content['dislike_count']
                article['create_time'] = article_content['create_time']
                article['last_update'] = article_content['last_update']
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
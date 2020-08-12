from flask import jsonify, request, current_app
from api import connection
from api.model.boardArticle import Category,Article,Article_disscuss
from flask_restful import Resource, reqparse
import re

class Index(Resource):
    def get(self):
        db = connection()
        cursor = db.cursor()
        sql = 'SELECT board_name, board_class FROM category'
        cursor.execute(sql)
        board_class = cursor.fetchall()
        disscussRank = list()
        for b in board_class:
            sql = "SELECT COUNT(*) FROM article_disscuss WHERE board_name = '%s'" % (b['board_name'])
            cursor.execute(sql)
            dissussCount = cursor.fetchone()
            insert = dict()
            insert['board_name'] = str(b['board_name'])
            insert['board_class'] = str(b['board_class'])
            insert['dissussCount'] = str(dissussCount['COUNT(*)'])
            disscussRank.append(insert)
        disscussRank.sort(key=lambda x:int(x['dissussCount']),reverse=True)

        sql = "SELECT DISTINCT board_name FROM category"
        cursor.execute(sql)
        distinct_board_name = cursor.fetchall()

        distinct_board_name_top = list()
        board_to_list = dict()
        for d in distinct_board_name:
            #sql = "select * from(select * from article order by push_count desc) as s group by board_name"
            sql = "SELECT * FROM article WHERE board_name = '%s' ORDER BY push_count DESC LIMIT 1" % (d['board_name'])
            cursor.execute(sql)
            d_result = cursor.fetchone()
            if d_result == None:
                continue
            else:
                """
                ip = d_result['author_ip']
                p1 = re.compile(r'[(](.*?)[)]', re.S)
                """
                d_result['author_ip'] = d_result['author_ip'].split('(')[-1].replace(')','')
                d_result['body'] = d_result['body'][0:101]
                d_result['article_url'] = '/' + d_result['board_name'] + '/' + d_result['article_number']

                sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='推 '" % (d_result['article_number'])
                cursor.execute(sql)
                like = cursor.fetchone()
                
                sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='→ '" % (d_result['article_number'])
                cursor.execute(sql)
                neutral = cursor.fetchone()

                sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='噓 '" % (d_result['article_number'])
                cursor.execute(sql)
                unlike = cursor.fetchone()

                d_result['like'] = like["COUNT(*)"]
                d_result['respone'] = neutral["COUNT(*)"]
                d_result['unlike'] = unlike["COUNT(*)"]

                del d_result['article_number']
                del d_result['last_update']
                del d_result['push_count']
                distinct_board_name_top.append(d_result)

        query_result = cursor.fetchall()
        cursor.close()
        package = dict()
        package['article'] = distinct_board_name_top
        for d in disscussRank[0:8]:
            d['board_url'] = '/board/' + d['board_name']
        package['hotboard'] = disscussRank[0:8]
        package['image'] = '/index.jpg'
        return jsonify(package)

class Board(Resource):
    def get(self,board_name):
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM article WHERE board_name = '%s'" % (board_name)
        cursor.execute(sql)
        query_result = cursor.fetchall()
        if query_result:
            package = dict()
            package['board'] = query_result
            cursor.close()
            return jsonify(package)
        else:
            return {'message':'board not found'},404

class All_board(Resource):
    def get(self):
        db = connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM category')
        category = cursor.fetchall()
        cursor.close()
        package = dict()
        package['all_board'] = category
        return jsonify(package)

class Article(Resource):
    def get(self,board,article_number):
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM article WHERE board_name = '%s' AND article_number = '%s'" % (board,article_number)
        cursor.execute(sql)
        if cursor.fetchone():
        #if article_number.startswith('M.'):
            sql = "SELECT * FROM article WHERE article_number = '%s'" % (article_number)
            cursor.execute(sql)
            article_content = cursor.fetchone()
            
            sql = "SELECT * FROM article_disscuss WHERE article_number = '%s'" % (article_number)
            cursor.execute(sql)
            disscuss = cursor.fetchall()

            sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='推 '" % (article_number)
            cursor.execute(sql)
            like = cursor.fetchone()
            
            sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='→ '" % (article_number)
            cursor.execute(sql)
            neutral = cursor.fetchone()

            sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='噓 '" % (article_number)
            cursor.execute(sql)
            unlike = cursor.fetchone()

            sql = "SELECT disscussion_id,from_pttLite,respone_type,respone_user_id,disscuss,respone_user_ip,create_time FROM article_disscuss WHERE article_number ='%s'" % (article_number)
            cursor.execute(sql)
            article_disscuss = cursor.fetchall()

            sql = "SELECT reply_id,article_disscussion_id,respone_type,respone_user_id,disscuss,respone_user_ip,create_time,last_update FROM reply_from_pttLite WHERE article_number ='%s'" % (article_number)
            cursor.execute(sql)
            reply_from_pttLite = cursor.fetchall()
            cursor.close()

            article = dict()
            article['article_url'] = '/' + article_content['board_name'] + '/' + article_content['article_number']
            article['board_name'] = article_content['board_name']
            article['article_number'] = article_content['article_number'] 
            article['title'] = article_content['title']
            article['author'] = article_content['author']
            article['author_ip'] = article_content['author_ip'].split('(')[-1].replace(')','')
            article['body'] = article_content['body']
            article['push_count'] = article_content['push_count']
            article['create_time'] = str(article_content['create_time'])
            article['disscuss'] = article_disscuss
            article['reply_from_pttLite'] = reply_from_pttLite 
            return jsonify(article)

        else:
            return {'message':'article not found'},404

def search():
    cursor = db.cursor()
    if request.method == 'POST':
        keyWord = request.form.get('keyWord')
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM article WHERE title LIKE '%s'" % ('%'+ keyWord +'%')
        cursor.execute(sql)
        searchingResult = cursor.fetchall()
        print(searchingResult)
        cursor.close()
        return jsonify('search.html',searchingResult=searchingResult)

class BoardToList(Resource):
    def get(self):
        db = connection()
        cursor = db.cursor()
        sql = "SELECT DISTINCT board_name FROM category ORDER BY board_name ASC"
        cursor.execute(sql)
        distinct_board_name = cursor.fetchall()

        board_to_list = dict()
        i = 0
        for d in distinct_board_name:
            board_to_list[str(d['board_name'])] = str(i)
            i += 1
        return jsonify(board_to_list)

class Article_Left_Join(Resource):
    def get(self,board,article_number):
        db = connection()
        cursor = db.cursor()
        sql = "SELECT * FROM article WHERE board_name = '%s' AND article_number = '%s'" % (board,article_number)
        cursor.execute(sql)
        if cursor.fetchone():
            sql = "SELECT * FROM article WHERE article_number = '%s'" % (article_number)
            cursor.execute(sql)
            article_content = cursor.fetchone()

            sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='推 '" % (article_number)
            cursor.execute(sql)
            like = cursor.fetchone()
            
            sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='→ '" % (article_number)
            cursor.execute(sql)
            neutral = cursor.fetchone()

            sql = "SELECT COUNT(*) FROM article_disscuss WHERE article_number = '%s' and respone_type='噓 '" % (article_number)
            cursor.execute(sql)
            unlike = cursor.fetchone()

            sql = "SELECT * FROM article_disscuss LEFT JOIN reply_from_pttLite ON article_disscuss.disscussion.id  = reply_from_pttLite.article_disscussion_id WHERE article_disscuss.article_number = '%s'" % (article_number)
            cursor.execute(sql)
            reply_from_pttLite = cursor.fetchall()
            cursor.close()

            article = dict()
            article['article_url'] = '/' + article_content['board_name'] + '/' + article_content['article_number']
            article['board_name'] = article_content['board_name']
            article['article_number'] = article_content['article_number'] 
            article['title'] = article_content['title']
            article['author'] = article_content['author']
            article['author_ip'] = article_content['author_ip'].split('(')[-1].replace(')','')
            article['body'] = article_content['body']
            article['push_count'] = article_content['push_count']
            article['create_time'] = str(article_content['create_time'])
            article['disscuss'] = reply_from_pttLite 
            return jsonify(article)

        else:
            return {'message':'article not found'},404

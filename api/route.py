from flask import jsonify, request, current_app
from api import getCursor
from api.model.boardArticle import Category,Article,Article_disscuss

def hotBoard():
    cursor = getCursor()
    sql = 'SELECT board_name, board_class FROM category'
    cursor.execute(sql)
    board_class = cursor.fetchall()
    #board_class = list( cursor.fetchall() )
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
    #disscussRank = sorted(disscussRank.items(), key=lambda x:x[1],reverse=True)
    disscussRank.sort(key=lambda x:int(x['dissussCount']),reverse=True)
    #return disscussRank[0:8]
    cursor.close()
    return disscussRank[0:8]
    
def index():
    cursor = getCursor()
    cursor.execute('select board_name,board_class from category;')
    category = cursor.fetchall()
    cursor.close()
    package = dict()
    package['article'] = category
    package['hotboard'] = hotBoard()
    package['image'] = '/index.jpg'
    return jsonify(package)

def all_board():
    cursor = getCursor()
    cursor.execute('select * from category;')
    category = cursor.fetchall()
    cursor.close()
    package = dict()
    package['all_board'] = category
    return jsonify(package)

def article(board,article_number):
    cursor = getCursor()
    sql = "SELECT * FROM article WHERE board_name = '%s' AND article_number = '%s'" % (board,article_number)
    cursor.execute(sql)
    if cursor.fetchone() != None:
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
        cursor.close()

        article = dict()
        article['board_name'] = article_content['board_name']
        article['article_number'] = article_content['article_number'] 
        article['title'] = article_content['title']
        article['author'] = article_content['author']
        article['author_ip'] = article_content['author_ip']
        article['body'] = article_content['body']
        article['push_count'] = article_content['push_count']
        article['create_time'] = article_content['create_time']
        article['last_update'] = article_content['last_update']
        return article
    
    else:
        return {'message':'article not found'},404

def search():
    cursor = getCursor()
    if request.method == 'POST':
        keyWord = request.form.get('keyWord')
        sql = "SELECT * FROM article WHERE title LIKE '%s'" % ('%'+ keyWord +'%')
        cursor.execute(sql)
        searchingResult = cursor.fetchall()
        print(searchingResult)
        cursor.close()
        return jsonify('search.html',searchingResult=searchingResult)
        """
        try:
            cursor.execute(sql)
            searchingResult = cursor.fetchall()
            cursor.close()
            return render_template('search.html',searchingResult=searchingResult)
        except Exception as e:
            print(e)
        """
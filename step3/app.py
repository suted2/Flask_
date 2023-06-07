from flask import Flask, render_template
from flask import request
from flask import flash
import pymysql 

name = ''

db_conn = pymysql.connect( # db 연결, info라는 이름의 db에 연결
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = '1234',
            db = 'info',
            charset = 'utf8' # 한글 깨짐 방지용 ! !
)

app = Flask(__name__) # 객체 생성 
app.secret_key = '1234'

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login_check', methods = ['POST'])
def login():
    global name 
    id_ = request.form["id"]
    pwd = request.form["pwd"]

    cursor = db_conn.cursor()

    query = "select * from User_info where user_id like '{}' and user_pwd like '{}'".format(id_, pwd)
    cursor.execute(query)

    if len(list(cursor)) > 0:
        name = id_
        cursor1 = db_conn.cursor()

        query = "select * from content"
        cursor1.execute(query)

        result = []
        for i in cursor1:
            temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
            result.append(temp)
        return render_template('notice_board.html', result_table = result)
    else:
        return render_template('main.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_add', methods=['POST'])
def signup_add():
    id_ = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    email = request.form['email']


    if id != '' and pwd != '' and name != '' and email != '':

        cursor = db_conn.cursor()

        query = "insert into User_info (user_id, user_pwd, user_name, user_email) values ('{}', '{}', '{}', '{}')".format(id_, pwd, name, email)

        cursor.execute(query)
        db_conn.commit()
        return render_template('main.html')

    else:
        flash("You need to fill all info")
        return render_template('signup.html')


@app.route('/notice_board') # 루트 경로
def notice_board(): #게시판 목록을 조회하기 위한 곳
    cursor = db_conn.cursor()

    query = 'select * from content'

    cursor.execute(query)

    result = []
    for i in cursor:
        temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
        result.append(temp)

    return render_template('notice_board.html', result_table = result)


@app.route('/notice_board_detail')
def notice_board_detail():
    temp = request.args.get('content_id')

    cursor = db_conn.cursor()

    query = "select * from content where content_id = {}".format(temp)

    cursor.execute(query)
    
    result = []
    for i in cursor:
        temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
        result.append(temp)

    return render_template('detail.html', result_table = result)

@app.route('/notice_board_add')
def notice_board_add():
    return render_template('add.html')

@app.route('/notice_board_add_check', methods = ['POST'])
def notice_board_add_check():
    global name
    title = request.form['title']
    string = request.form['content']

    if title != '' and string != '':
        cursor = db_conn.cursor()

        query = 'select * from content'
        cursor.execute(query)
        for i in cursor:
            num = i[0]
        query1 = "insert into content (content_id, user_id, content_title, content_string) values ('{}', '{}', '{}', '{}')".format(num+1, name ,title, string)

        cursor.execute(query1)
        db_conn.commit()

        cursor = db_conn.cursor()

        query2 = 'select * from content'
        cursor.execute(query2)

        result = []
        for i in cursor:
            temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
            result.append(temp)

        return render_template('notice_board.html', result_table = result)
    else:
        flash("You need to fill all info")
        return render_template('add.html')

@app.route('/notice_board_delete')
def notice_board_delete():
    temp = request.args.get('content_id')

    cursor = db_conn.cursor()

    query = "delete from content where content_id = {}".format(temp)

    cursor.execute(query)
    db_conn.commit()
    cursor = db_conn.cursor()

    query = 'select * from content'
    cursor.execute(query)

    result = []
    for i in cursor:
        temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
        result.append(temp)


    return render_template('notice_board.html', result_table = result)

@app.route('/update', methods = ['POST'])
def notice_board_fix():
    temp = request.args.get('content_id') # 현재 수정하려고 하는 게시글의 id를 받아옴

    content_tit = request.form['content_title'] # 수정하려고 하는 제목 
    content_str = request.form['content_string'] # 수정하려고 하는 게시글 내용

    if content_tit != '': # 게시글 제목을 변경하겠다 ! 
        cursor = db_conn.cursor()
        query = "update content set content_title = '{}' where content_id like '{}'".format(content_tit, temp)
        cursor.execute(query)

    if content_str != '':

        cursor = db_conn.cursor()
        query = "update content set content_string = '{}' where content_id like '{}'".format(content_str, temp)
        cursor.execute(query) 

    cursor = db_conn.cursor()

    query = "select * from content where content_id like '{}'".format(temp)

    cursor.execute(query)
    
    result = []
    for i in cursor:
        temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
        result.append(temp)

    return render_template('detail.html', result_table = result)



if __name__ == "__main__": # 메인함수 지정 
    app.run(debug=True)
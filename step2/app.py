from flask import Flask, render_template
from flask import request
import pymysql 

db_conn = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = '1234',
            db = 'test',
            charset = 'utf8' # 한글 깨짐 방지용 ! !
)

print(db_conn)

#커서 객체 생성


app = Flask(__name__)

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signupPost():
    uid= request.form['user_id'] # name이 user_id인 폼 값을 가져와라
    upwd= request.form['user_pwd']
    uemail= request.form['user_email']
    uphone= request.form['user_phone']
    print(uid, upwd, uemail, uphone)

    return render_template("signup.html")


@app.route('/sqltest')
def sqltest():
    cursor = db_conn.cursor()

    query = "select * from player"

    cursor.execute(query)
    
    result = []
    for i in cursor:
        temp = {'player_id':i[0], 'player_name':i[1] }
        result.append(temp)

    return render_template('sqltest.html', result_table=result)

@app.route('/detail')
def detailtest():
    temp = request.args.get('id')
    temp1 = request.args.get('name')

    cursor = db_conn.cursor()

    query = "select * from player where player_id = {} and player_name like '{}'".format(temp, temp1)
    cursor.execute(query)

    result = []
    for i in cursor:
        temp = {'player_id':i[0], 'player_name':i[1], 'team_name':i[2], 'height':i[-2], 'weight':i[-1] }
        result.append(temp)

    return render_template('detail.html', result_table = result)



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="127.0.0.1", port="7000")
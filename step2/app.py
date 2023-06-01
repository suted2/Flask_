from flask import Flask, render_template
from flask import request
import pymysql 

db_conn = pymysql.connect(
            host = 'localhost',
            port = 3306, #sql 기본 port  개인마다 다를 수 있음 .
            user = 'root',
            passwd = '1234',
            db = 'test', # 우리가 연동하려는 데이터 테이블을 가지고 온다. 
            charset = 'utf8' # 한글 깨짐 방지용 ! !
)

print(db_conn)

#커서 객체 생성


app = Flask(__name__)

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"]) # POST 방식의 정보 전달일때는 표기를 해준다. 
def signupPost():
    uid= request.form['user_id'] # name이 user_id인 폼 값을 가져와라
    upwd= request.form['user_pwd']
    uemail= request.form['user_email']
    uphone= request.form['user_phone']
    print(uid, upwd, uemail, uphone)

    return render_template("signup.html")


@app.route('/sqltest')
def sqltest():
    cursor = db_conn.cursor() #cursor() 객채를 생성해준다. 

    query = "select * from player" # 명령어 작성 

    cursor.execute(query) # 해당 명령어 실행 
    
    result = []
    for i in cursor:
        temp = {'player_id':i[0], 'player_name':i[1] } #GET 함수이기도 하고 list에 들어있기에 가지고 온다. 
        result.append(temp)

    return render_template('sqltest.html', result_table=result) # 결과값이 table 형태이기에 result_table = result 를 줘서 진행한다. 

@app.route('/detail')
def detailtest():
    temp = request.args.get('id') # 해당 정보 역시 get 방식의 전달이기에 해당 방식을 사용해 진행한다. 
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
    app.run(host="127.0.0.1", port="7000") ## 임의로 host, 와 port를 지정해서 변경할 수 있다. 
                                           ## host를 지정할때 다른 프로그램과 충돌이 있을 수 있어 확인해야한다. 

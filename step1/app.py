# app.py 백엔드에 해당하는 파일 

from flask import Flask, render_template 
from flask import request
# Flask 객체 인스턴스 생성

app = Flask(__name__)

@app.route('/main') # 접속하는 url 바인딩 .
def index():
    temp = request.args.get('uid')  #링크에 담긴 변수의 값을 가지고 올 수 있다. 
    temp1 = request.args.get('cid') 

    print(temp, temp1)

    return render_template('index.html') 

@app.route('/test')
def testget():

    return render_template('posttest.html')



@app.route('/test', methods=['POST'])
def testget1():
    value = request.form['input']

    print(value)

    return render_template('posttest.html')


if __name__ == "__main__":
    app.run(debug=True) 
    # debug=True : 코드가 수정될 때마다 서버가 재시작됨
    # 서버가 실행되면 http://
    # host 등을 직접 지정하고 싶다면
    # app.run(host = '127.0.0.1", port = 5000, debug = True)
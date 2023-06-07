## What we do



### 로그인 화면과 게시판 화면을 구현하는 연습을 한다. 


#### FLow 1. main login 화면을 만든다. 

![로그인 화면](https://github.com/suted2/Flask_/assets/101646531/d1421520-c282-455a-b0a7-28545b6a04b9)

해당 화면을 만들어 준다. 

```html 
<!DOCTYPE html>

<html>
    <header>
        <title>로그인 화면</title>
    </header>



    <body>
        <div style = 'text-align: center'>
        <h1>로그인</h1>
        
            <form action="login_check" method = "post">
                <input type="text" name = "id" placeholder="아이디"> <br>
                <input type="password" name = "pwd" placeholder="비밀번호"> <br>
                <input type="submit" value ='Login'> <br>
    
            </form>
        
            <button type="button" onClick="location.href='/signup'">회원가입</button>
        
        </div>
    </body>
</html>

```


다음과 같이 구성을 해주고 , 아이디, 비밀번호 창에 id를 넣으면 login_check 가 구동되도록 지정된다. 



#### FLow 2. login_check 함수를 만든다. 


```python

@app.route('/login_check', methods = ['POST']) # login_check에 대응
def login():
    global name 
    id_ = request.form["id"] # 이전 로그인 페이지가 POST방식이기에 name이 id인 정보 가지고 온다. 
    pwd = request.form["pwd"] # 이전 로그인 페이지가 POST방식이기에 name이 pwd인 정보 가지고 온다. 

    cursor = db_conn.cursor() 

    query = "select * from User_info where user_id like '{}' and user_pwd like '{}'".format(id_, pwd)
    cursor.execute(query) #위에서 받은 정보를 통해 SQL 데이터 베이스에서 검색을해서 

    if len(list(cursor)) > 0:  # cursor의 len이 1 이상이라는 것은 우리가 찾은 회원 정보가 이미 있는것
        name = id_ 
        cursor1 = db_conn.cursor()

        query = "select * from content"
        cursor1.execute(query)

        result = []
        for i in cursor1:
            temp = {'content_id' : i[0], 'user_id': i[1],  'content_title' : i[2],  'content_string' : i[3]}
            result.append(temp)
        return render_template('notice_board.html', result_table = result) #로그인에 성공한다면 후에 보여줄 게시글 페이지로 넘어가게 해준다. 
    else: #아니라면 없는 정보이기에 main화면으로 돌려준다. 
        return render_template('main.html')
```

다음과 같이 로그인 check함수를 구현해 준다. 



#### Flow 3. 아이디가 애초에 없다면 회원가입을 시도해야 한다. 



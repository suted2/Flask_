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

![회원가입 화면](https://github.com/suted2/Flask_/assets/101646531/8a5454a8-56e7-481f-aa58-84dc08da4596)

```html
<!DOCTYPE html>
<html>
    <head>
        <title>회원가입</title>
    </head>

    <body>
        <div style ="text-align: center;">
        <h1> 회원가입</h1>
            <form action ='signup_add' method ="post">  <!--회원 가입을 위한 정보를 기입하는 장소이다.  -->
                <input type="text" name = 'id' placeholder="아이디"> <br> 
                <input type="password" name = 'pwd' placeholder="비밀번호"> <br>
                <input type="text" name = 'name' placeholder="이름"> <br>
                <input type="text" name = 'email' placeholder="이메일"> <br>

                <input type="submit" value ='회원가입' onclick="alert('회원 가입 완료')">  <!--정보를 전부 기입하고 회원가입을 눌렀을때 알림창을 준다. -->
            </form>
    </body>
</html>

```


```python 

@app.route('/signup_add', methods=['POST'])
def signup_add(): # 위의 html 화면에서 입력한 정보를 더하고 
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

```



#### Flow 4. 게시판 목록에서 자세히 보기 / 수정할 수 있는 양식을 만든다.  

![게시글 목록](https://github.com/suted2/Flask_/assets/101646531/03b0eb44-9e96-424d-9e4c-8ae19bf8a553)


```html
<body>

<!-- 게시글 작성-->
<div style ="text-align: center;">

    <h3>게시글 작성</h3>
    <button onClick="location.href='/notice_board_add'">게시글 작성</button> <!--게시글 작성을 위한  추가 버튼생성-->
    </div>


<table>
    <tr>
        <th>Num</th>
        <th>게시물 제목</th>
        <th>유저번호</th>
    </tr>
        {% for row in result_table%}
        <tr>
            <td>{{row.content_id}}</td>
            <td>{{row.content_title}}</td>
            <td>{{row.user_id}}</td>
            <td><button onClick="location.href='/notice_board_detail?content_id={{row.content_id}}'">상세보기</button></td>
            <td><button onClick="location.href='/notice_board_delete?content_id={{row.content_id}}'">삭제</button></td>

        </tr>
        {% endfor %}
</table>

```




```python
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


```






#### Flow 4-2. 게시판 상세 보기 확인 

![](https://github.com/suted2/Flask_/assets/101646531/de5fce33-ad2e-427e-b6a9-bc905f6f2761)


```html
<!DOCTYPE html>

<html>
<head>
<style>
table, th, td, tr{
    border : 1px solid black
}
</style>
<meta charset="UTF-8">
<title>게시물 상세읽기</title>
</head>

<body>
<table>
    <tr>   <!--원하는 정보를 표현하기 위한 테이블 생성--> 
        <th>게시판 번호</th>
        <th>유저 id</th>
        <th>게시물 제목</th>
        <th>게시글 내용</th>
    </tr>

        {% for row in result_table%}
        <tr>
            <td>{{row.content_id}}</td>
            <td>{{row.user_id}}</td>
            <td>{{row.content_title}}</td>
            <td>{{row.content_string}}</td>

        </tr>
        {% endfor %}
</table>


<h2>게시글 수정</h2> <!--수정을 위한 테이블 만들기 .-->
<table>
    <tr>
        <th>게시물 번호</th>
        <th>게시글 제목</th>
        <th>게시글 내용</th>
        <th>    </th>

    </tr>

    {% for row in result_table%}
    
    
    <form action="/update?content_id={{row.content_id}}" method="post"> <!--수정을 누르는 순간 /update가 발동된다. -->
        <tr>
            <td>{{row.content_id}}</td>
            <td><input type="text" name="content_title"></input></td>
            <td><input type="text" name="content_string"></input></td>
            <td><input type="submit" value="수정"></input></td>
        </tr>
    </form>
    {% endfor %}
</table>

<h3>원래 페이지로</h3>
<button onClick="location.href='/notice_board'">돌아가기</button>

<img src ="{{ url_for('static', filename = 'IMG/puppy.jpg')}}" width="300" height="300"> <!--원래 게시글로 돌아가기 위한 버튼을 제공한다.-->



</body>
</html>

```

```python

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

```



---

```python
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


```


게시글을 추가하기 위한 글 

🤔 Discussion 

1. Login ID의 경우 session으로 관리하지만 해당 과정에 대한 진도는 나가지 않아. 
일단 get으로 넘기기 보다는 python 파일에서 전역변수를 사용하여 해당 전역변수에서 id를 저장하고 게시글에 쓸때까지 가져온다. 

2. 게시판 NUm을 유지하기 위해 가장 먼저는 len(list(cursor))를 통해 현재 게시글의 숫자를 count했지만 이럴경우 삭제가 일어나면 오류가 생긴다 따라서 해당 함수를 
list(cursor)의 마지막 num을 가지고 와서 +1 하는 방식으로 수정하여 해결 할 수 있었다. 



----

### img, 동영상 넘기기 

1. 기본적으로 image, video , css, 등등의 경우는 static / 함수 아래 적용하고 keep을 했다. 

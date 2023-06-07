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

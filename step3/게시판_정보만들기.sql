create database info;
use info;


create table User_info(
	user_id varchar(20) not null primary key,
    user_name varchar(20) not null,
    user_pwd varchar(20) not null,
    user_email varchar(20) not null
    );


create table content(
	content_id int primary key,
    user_id varchar(20) not null,
    content_title varchar(20) not null,
    content_string varchar(20) not null,
    
    constraint content_FK foreign key (user_id) references User_info(user_id)
);



INSERT INTO User_info VALUES ('0000001','황민규','1234','0beloved0@naver.com');

INSERT INTO content VALUES ('1000001','0000001','부트캠프 어디가 좋은가요','부트캠프가려고 하는데 어디가 좋음');
INSERT INTO content VALUES ('1000002','0000001','오늘 저녁뭐먹지..','추천좀');
INSERT INTO content VALUES ('1000003','0000001','뭐하구있음','오늘 비올듯');


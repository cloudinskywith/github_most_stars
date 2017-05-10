本教程基于Ubuntu16.04

### 1.安装postgresql
`sudo apt-get install postgresql-client`
`sudo apt-get install postgresql`

### 2.增加postgresql用户
```
$ sudo su - postgres #切换到postgres超级用户

$ psql               #进入控制台

postgres=# \password postgres   #输入  \password为postgres设置密码
Enter new password:  postgres   #为了方便，密码也设置为postgres
Enter it again: postgres        #再次输入密码

postgres=# create user myuser with password myuser;  #创建密码为myuser名为myuser的用户
```

### 3.创建数据并赋权限
```
postgres=# create database my_test owner myuser;               #给myuser用户创建my_test的数据库
postgres=# grant al privileges on database my_test on myuser;  #将该数据库所有权限给myuser
```

### 4.CRUD
```
postgres=# drop database if exists puppy;                     #如果puppy数据库存在，删除
postgres=# \c database_name;                                  #连接名为database_name的数据库
postgres=# create table pups(id serial primary key,name varchar,breed varchar, age integer,sex varchar);  #建表
postgres=# insert into pups(name,breed,age,sex) values('kyle','seek',3,'m')
```


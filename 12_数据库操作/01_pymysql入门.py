#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 1:05
# @Author  : fuqingyun
# @File    : 01_pymysql入门.py
# @Description :

from pymysql import Connection

# 构建MySQL的数据库连接
conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    autocommit=True #设置自动提交
)

print(conn.get_server_info())  # 8.0.38

# 执行非查询性质sql
cursor = conn.cursor()  # 获取到游标对象

# 选择数据库
conn.select_db('world')

# 执行sql
# cursor.execute('create table test_pymysql(id int);')
# cursor.execute('create table test_pymysql2(id int)')

# 执行查询性质sql
cursor.execute('select * from city')
results=cursor.fetchall()
# print(results)
for r in results:
    print(r)

# 执行插入操作
cursor.execute("insert into student values(10001,'周杰伦',31)")
# 通过commit确认提交修改
# conn.commit()

# 关闭数据库的连接
conn.close()

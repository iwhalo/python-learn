#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/29 14:33
# @Author  : fuqingyun
# @File    : 02_main.py
# @Description : SQL综合案例，读取文件，写入MySOL数据库中

from data_define import *
from file_define import *

from pymysql import Connection

text_file_reasder = TextFileReader('')
json_file_reader = JsonFileReader('')

jan_data: list[Record] = text_file_reasder.read_data()
feb_data: list[Record] = json_file_reader.read_data()

all_data: list[Record] = jan_data + feb_data

# 构建MySQL连接
conn = Connection(
    host='localhost',
    user='root',
    password='123456',
    autocommit=True
)

# 获得游标对象
cursor = conn.cursor()
# 选择数据库
conn.select_db('py_mysql')
# 组织sql语句
for record in all_data:
    sql = f"insert into orders(order_date,order_id,money,province) values ('{record.date}','{record.order_id}',{record.money},'{record.province}')"
    # print(sql)
    cursor.execute(sql)

# 关闭MySQL连接对象
conn.close()

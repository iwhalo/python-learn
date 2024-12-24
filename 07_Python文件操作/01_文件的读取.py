#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_文件的读取.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 20:16 
@Function:
'''
import time

# 打开文件
f = open('../notes/note.md', 'r', encoding='UTF-8')
print(type(f))  # <class '_io.TextIOWrapper'>
# 读取文件 - read()
# content = f.read(10)  # 不传值的话读取文件中所有数据内容，传参表示要从文件中读取的数据的长度（单位是字节），如果没有传入num,那么就表示读取文件中所有的数据。
# print(f"读取10个字节的结果：{content}")
# print(f"read方法读取全部内容的结果：{f.read()}")  # 当前read会从上个read读取的内容之后开始读取数据
print('==========================================')
# 读取文件 - readLines()
# readlines可以按照行的方式把整个文件中的内容进行一次性读取，并且返回的是一个列表，其中每一行的数据为元素。
lines = f.readlines()  # 读取文件的全部行封装到列表中（注意：这里，当前readlines会从上个read读取的内容之后开始读取数据，此时读取的内容是空的，注释掉16、18行代码即可）
print(f"lines对象的类型是：{type(lines)}")
print(f"lines对象的内容是：{lines}")

# 读取文件 - readLine()
# readline方法：一次读取一行内容
f = open('../notes/note.md', 'r', encoding='UTF-8')
line1=f.readline()
print(line1)
line2=f.readline()
print(line2)

# for循环读取文件行
f = open('../notes/note.md', 'r', encoding='UTF-8')
for line in f:
    print(f"当前行数据是：{line}")

# 文件的关闭
f.close()

# with open 语法操作文件
# 该方法会自动执行close方法
with open('../notes/note.md','r',encoding='UTF-8') as f:
    for line in f:
        print(f"当前行数据是：{line}")

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：02_Python函数参数的多种使用形式.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 19:17 
@Function:
'''

def user_info(name,age,gender):
    print(f"姓名是：{name}，年龄是：{age}，性别是：{gender}")

# 位置参数 - 默认使用形式
user_info('小明',18,'男')  #必须按照参数定义顺序来传参
# user_info(18,'男','小明')

# 关键字参数
user_info(name='小王',age='18',gender='男')
user_info(age=18,name='晓晓',gender='女')  # 可以不按照参数定义顺序来传参
user_info('田田',age=18,gender='女')

# 缺省参数（默认值）
def user_info(name,age,gender='男'):
    print(f"姓名是：{name}，年龄是：{age}，性别是：{gender}")

user_info('小甜',13)
user_info('小甜',13,'女')
user_info('小甜',13,gender='女')

# 不定长 - 位置不定长，*号
# 不定长定的形式参数会作为元组存储，接收不定长数量的参数
def user_info(*args):
    print(f"args参数的类型是：{type(args)}，内容是：{args}")

user_info(1,2,3,'小明','男')

# 不定长 - 关键字不定长，**号
def user_info(**kwargs):
    print(f"kwargs参数的类型是：{type(kwargs)}，内容是：{kwargs}")

user_info(name='小王',age=11,gender='男')
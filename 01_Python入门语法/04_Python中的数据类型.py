#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_Python中的数据类型.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/26 21:13 
@Function:
'''

# 使用print直接输出类型信息
print(type("黑马程序员"))
print(type(666))
print(type(13.14))
# 使用变量存储type()语句的结果
string_type = type("黑马程序员")
int_type = type(666)
float_type = type(13.14)
print(string_type)
print(int_type)
print(float_type)
# 使用type()语句，查看变量中存储的数据类型信息
name = "黑马程序员"
name_type = type(name)
print(name_type)

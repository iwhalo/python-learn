#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_Python字符串课后练习.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/2/1 19:59 
@Function:
'''
my_str="itheima itcast boxuegu"

# 统计字符串中有多少个"it"字符
num=my_str.count("it")
print(f"字符串{my_str}中有{num}个it字符")

# 将字符串内的空格全部替换为字符：“|”
new_my_str=my_str.replace(" ","|")
print(f"字符串{my_str}替换空格后，结果是{new_my_str}")

# 并按照“|”进行字符串分割，得到列表
my_str_list=new_my_str.split("|")
print(f"将字符串{new_my_str}按照|进行分割后得到列表：{my_str_list}")


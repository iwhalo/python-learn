#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_Python数据容器之序列的切片练习.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/2/1 20:59 
@Function:
'''


my_str="万过薪月，员序程马黑来，nohtyP学"

# 倒序字符串，切片取出
my_str1=my_str[::-1]
print(my_str1)

my_str2=my_str1[9:14]
print(my_str2)

# split分割“, ”，replace替换“来”为空，倒序字符串
my_str3=my_str.split("，")[1].replace("来","")[::-1]
print(my_str3)
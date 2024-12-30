#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_正则表达式_基础匹配.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 19:40 
@Function:
'''

import re

s1 = "python itheima"
s2 = "1python itheima python python"

# match从头匹配
result = re.match("python", s1)  # <re.Match object; span=(0, 6), match='python'>
print(result)
print(result.span())  # (0, 6)
print(result.group())  # python
print("=================================")

# match从头匹配,头部开始就匹配不上，后面也不会匹配
result = re.match("python", s2)  # None
print(result)
print("=================================")

# search搜索整个字符串，找出匹配的。从前向后，找到第一个后，就停止，不会继续向后
result = re.search("python", s2)
print(result)  # <re.Match object; span=(1, 7), match='python'>
print("===========================================")

# findall 匹配整个字符串，找出全部匹配项
result = re.findall("python", s2)
print(result)  # ['python', 'python', 'python']

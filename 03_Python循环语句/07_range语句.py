#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_range语句.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/5 20:28 
@Function:
'''
import task as task

# 语法1：range(num)

for x in range(10):
    print(x)


# 语法2：range(num1, num2)


for x in range(5,10):
    print(x)

# 语法3：range(num1, num2, step)

for x in range(5,10,2):
    print(x)

for x in range(10):
    print("送玫瑰花")
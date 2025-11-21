#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_range语句使用_1到100有几个偶数.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/5 20:34 
@Function:
'''
count = 0
for x in range(1, 100):
    if x % 2 == 0:
        print(x)
        count += 1
print(f"1到100一共有{count}个偶数")

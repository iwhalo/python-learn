#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_for循环数一数有几个a.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/5 20:15 
@Function:
'''


name="itheima is a brand of itcast"
count=0

for x in name:
    print(x)
    if x=="a":
        count+=1
print(f"一共有{count}个a!")
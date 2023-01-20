#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_for循环临时变量作用域.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/18 14:07 
@Function:
'''

i = 0

for i in range(5):
    print(i)

print(i)

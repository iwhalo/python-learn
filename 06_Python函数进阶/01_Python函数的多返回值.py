#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_Python函数的多返回值.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 18:18 
@Function:
'''

def test_return():
    return 1,2,3

x,y,z=test_return()
print(x)
print(y)
print(z)
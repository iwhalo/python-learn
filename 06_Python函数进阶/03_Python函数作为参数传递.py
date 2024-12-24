#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_Python函数作为参数传递.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 19:45 
@Function:
'''

# 定义一个函数，接收另一个函数作为传入参数
def test_func(compute):
    result=compute(1,2)
    print(f"compute参数的类型是：{type(compute)}")
    print(f"计算结果是：{result}")

# 定义一个函数，准备作为参数传入另一个函数
def compute(x,y):
    return x+y

# 调用，并传入函数
test_func(compute)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_类型注解_函数(方法)的形参_返回值的注解.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 15:54 
@Function:
'''


# 对形参进行类型注解
def add(x: int, y: int):
    return x + y


add(1, 2)


# 对返回值进行类型注解
def func(data: list) -> list:
    return data

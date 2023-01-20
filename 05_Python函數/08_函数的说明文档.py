#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_函数的说明文档.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/20 9:46 
@Function:
'''


# 定义函数，进行文档说明

def add(x, y):
    """
    add函数可以接收两个参数，进行两数相加的功能
    :param x:形参x表示想加的其中一个数字
    :param y:形参y表示想加的两一个数字
    :return:返回值是两数相加的结果
    """
    result = x + y
    print(f"{x} + {y} = {result}")
    return result


add(5, 6)

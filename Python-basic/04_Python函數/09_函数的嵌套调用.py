#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_函数的嵌套调用.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/20 9:53 
@Function:
'''


# 定义函数func_b
def func_b():
    print("--------2---------")

#定义函数func_a，并在内部调用func_b
def func_a():
    print("--------1---------")

    # 嵌套调用func_b
    func_b()

    print("--------3---------")


# 调用函数func_a
func_a()

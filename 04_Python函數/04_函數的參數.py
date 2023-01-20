#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_函數的參數.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/19 16:09 
@Function:
'''


def add(x,y):
    result=x+y
    print(f"{x} + {y}的計算結果是：{result}")

a=int(input("請輸入第一個數："))
b=int(input("請輸入第二個數："))
add(a,b)
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_Python中的字符串格式化的精度控制.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/27 21:25 
@Function:
'''

num1 = 11
num2 = 11.345
print("数字11宽度限制5，结果是：%5d" % num1)
print("数字11宽度限制1，结果是：%1d" % num1)   #m比数字本身宽度还要小，相当于没有写m
print("数字11.345宽度限制7，小数精度2，结果是：%7.2f" % num2)
print("数字11.345宽度不限制，小数精度2，结果是：%.2f" % num2)

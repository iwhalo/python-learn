#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：15_Python中的input语句.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/28 20:02 
@Function:
'''

print("请告诉我你是谁？")
name = input()
print("我知道了，你是：%s" % name)

name = input("请告诉我你是谁？")
print("我知道了，你是：%s" % name)

# 输入数字类型
num = input("请告诉我你的银行卡密码：")
print("你的银行卡密码类型是：", type(num))

num = input("请告诉我你的银行卡密码：")
# 数据类型转换
num=int(num)
print("你的银行卡密码类型是：", type(num))

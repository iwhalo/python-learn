#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_猜猜心里数字.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/4 20:36 
@Function:
'''


# 定义一个变量
num=5

# 通过键盘输入获取猜想的数字，通过多次if和elif的组合进行猜想比较
if int(input("请猜一个数字："))==num:
    print("恭喜第一次就猜对了！")
elif int(input("猜错了，再猜一次："))==num:
    print("猜对了")
elif int(input("猜错了，再猜一次："))==num:
    print("恭喜，最后一次机会，你猜对了！")
else:
    print("Sorry, 猜错了")
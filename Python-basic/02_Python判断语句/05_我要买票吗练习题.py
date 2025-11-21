#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_我要买票吗练习题.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/29 20:49 
@Function:
'''

# 定义键盘输入获取身高数据
height = int(input("请输入你的身高（cm）："))

# 通过if进行判断
if height > 120:
    print("您的身高超出120cm，游玩需要购票10元。")
else:
    print("您的身高未超出120cm，可以免费游玩。")

print("祝您游玩愉快。")

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_if_elif_else语句的使用.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/29 21:01 
@Function:
'''

# height = int(input("请输入您的身高（cm）："))
# vip_level = int(input("请输入你的VIP等级（1-5）："))
#
# day = int(input("请告诉我今天几号："))

# 通过if判断可以使用多条件判断的语法
# 第一个条件就是if
# if height < 120:
#     print("身高小于120cm，可以免费。")
# elif vip_level > 3:
#     print("vip等级大于3，可以免费。")
# elif day == 1:
#     print("今天是1号免费日，可以免费。")
# else:
#     print("不好意思，条件都不满足，需要买票10元。")
#
# print("祝您游玩愉快。")



if int(input("请输入您的身高（cm）：")) < 120:
    print("身高小于120cm，可以免费。")
elif int(input("请输入你的VIP等级（1-5）：")) > 3:
    print("vip等级大于3，可以免费。")
elif int(input("请告诉我今天几号：")) == 1:
    print("今天是1号免费日，可以免费。")
else:
    print("不好意思，条件都不满足，需要买票10元。")

print("祝您游玩愉快。")
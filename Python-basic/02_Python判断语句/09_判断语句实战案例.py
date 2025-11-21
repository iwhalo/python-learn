#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_判断语句实战案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/4 21:01 
@Function:
'''

# 1、构建一个随机数字变量
import random
num=random.randint(1,10)
print(num)

guess_num=int(input("输入你要猜测的数字："))

# 2、通过if判断语句进行数字的猜测
if guess_num==num:
    print("恭喜你，第一次就猜对了！")
else:
    if guess_num<num:
        print("你猜测的数字太小了！")
    else:
        print("你猜测的数字太大了！")

    guess_num=int(input("再次输入你要猜测的数字："))
    if guess_num == num:
        print("恭喜你，第二次猜中了！")
    else:
        if guess_num < num:
            print("你猜测的数字太小了！")
        else:
            print("你猜测的数字太大了！")

    guess_num = int(input("再次输入你要猜测的数字："))
    if guess_num == num:
        print("恭喜你，第三次猜中了！")
    else:
        if guess_num < num:
            print("你猜测的数字太小了！")
        else:
            print("你猜测的数字太大了！")
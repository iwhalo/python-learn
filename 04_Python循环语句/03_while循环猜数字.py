#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_while循环猜数字.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/5 19:01 
@Function:
'''
import random

num = random.randint(1,10)

# guess_num=int(input("输入你猜测的数字："))
#
# while guess_num!=num:
#     if guess_num>num:
#         print("你猜测的数字大了")
#     else:
#         print("你猜测的数字小了")
#     guess_num=int(input("再次输入你要猜测的数字："))
#
# print("恭喜你，猜对了！")


flag=True
count=0

while flag:
    guess_num=int(input("再次输入你要猜测的数字："))
    count+=1

    if guess_num==num:
        print("恭喜你，猜对了！")
        flag=False
    else:
        if guess_num > num:
            print("你猜测的数字大了")
        else:
            print("你猜测的数字小了")

print(f"一共猜了 {count} 次")

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：12_循环中断.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/18 14:44 
@Function:
'''


# 演示循环中断语句  continue
# for i in range(1,6):
#     print("语句1")
#
#     continue
#
#     print("语句2")


# 演示continue的嵌套应用
for i in range(1,6):
    print("语句1")

    for j in range(1,6):
        print("语句2")
        continue
        print("语句3")

    print("语句4")

# for i in range(1,101):
#     print("语句1")
#     break
#     print("语句2")
#
# print("语句3")


# for i in range(1,6):
#     print("语句1")
#     for j in range(1,6):
#         print("语句2")
#         break
#         print("语句3")
#
#     print("语句4")
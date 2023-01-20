#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_Python中的各类运算符.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/27 20:32 
@Function:
'''

# 算数（数学）运算符
print("1 + 1 = ", 1 + 1)
print("2 - 1 = ", 2 - 1)
print("3 * 3 = ", 3 * 3)
print("4 / 2 = ", 4 / 2)
print("11 // 2 = ", 11 // 2)
print("9 % 2 = ", 9 % 2)
print("3 ** 2 = ", 3 ** 2)

# 赋值运算符
num = 1 + 2 * 3
# 复合赋值运算符
# +=
num = 1
num += 1
print("num += 1: ", num)
num -= 1
print("num -= 1: ", num)
num *= 4
print("num *= 4: ", num)
num /= 2
print("num /= 2: ", num)
num = 3
num %= 2
print("num %= 2: ", num)

num **= 2
print("num **= 2: ", num)

num = 9
num //= 2
print("num //= 2: ", num)

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
a=1
b=2
c=a+b
print(a,b,c,1000,sep='#')
print(a,b,c,1000)

a=input('键盘输入任意整数，判断该数字的奇偶性：')
print('打印其个位数为：',int(a)%10)
print('打印其十位数为：',int(a)%100//10)
print('打印其百位数为：',int(a)//100)
b=int(a)%2
if b==0:
    print('您所输入的数字'+a+'为偶数')
else:
    print('您所输入的数字'+a+'为奇数')

print('=============================================')

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

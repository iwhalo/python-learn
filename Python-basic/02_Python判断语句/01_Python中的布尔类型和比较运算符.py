#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_Python中的布尔类型和比较运算符.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/29 20:19 
@Function:
'''

# 定义变量存储布尔类型的数据
bool_1 = True
bool_2 = False
print(f"bool_1变量的内容是：{bool_1}，类型是：{type(bool_1)}")
print(f"bool_2变量的内容是：{bool_2}，类型是：{type(bool_2)}")

# 内容的相等比较
num1 = 10
num2 = 10
print(f"10 == 10的结果是：{num1 == num2}")

num1 = 10
num2 = 15
print(f"10 != 15的结果是：{num1 != num2}")

name1 = "itcast"
name2 = "itheima"
print(f"itcast == itheima的结果是：{name1 == name2}")

# 大于、小于、大于等于、小于等于
num1 = 10
num2 = 15
print(f"10 > 15的结果是：{num1 > num2}")
print(f"10 < 15的结果是：{num1 < num2}")

num1 = 10
num2 = 10
print(f"10 >= 10的结果是：{num1 >= num2}")
print(f"10 <= 10的结果是：{num1 <= num2}")

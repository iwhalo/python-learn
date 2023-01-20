#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_变量的作用域.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/20 10:01 
@Function:
'''


# 演示局部变量
def test_A():
    num1 = 100
    print(num1)


test_A()
# print(num1)  #NameError: name 'num' is not defined

# 演示全局变量
num2 = 200


def test_a():
    print(f"test_a():{num2}")


def test_b():
    print(f"test_b():{num2}")


test_a()
test_b()
print(num2)

# 在函数内修改全局变量
num2 = 200

def test_a():
    print(f"test_a():{num2}")


def test_b():
    num2 = 500  #局部变量。在函数内修改全局变量，还是局部变量，函数外调用全局变量依然没有改变
    print(f"test_b():{num2}")


test_a()
test_b()
print(num2)

# global关键字，在函数内声明变量为全局变量
num2 = 200

def test_a():
    print(f"test_a():{num2}")


def test_b():
    global num2 #设置内部定义的变量为全局变量
    num2 = 500
    print(f"test_b():{num2}")


test_a()
test_b()
print(num2)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_闭包.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 20:24 
@Function: 演示Python的闭包特性
'''


# 简单闭包
def outer(logo):
    def inner(msg):
        print(f"<{logo}>{msg}<{logo}>")

    return inner


fn1 = outer("黑马程序员")
fn1("大家好")


# 使用nonlocal关键字修改外部函数的值
def outer(num1):
    def inner(num2):
        nonlocal num1
        num1 += num2
        print(num1)

    return inner


fn = outer(10)
fn(20)


# 使用闭包实现ATM案例

def account_creat(initial_aamount=0):
    def atm(num, deposit=True):
        nonlocal initial_aamount
        if deposit:
            initial_aamount += num
            print(f"存款：+{num},账户余额：{initial_aamount}")
        else:
            initial_aamount -= num
            print(f"取款：-{num},账户余额：{initial_aamount}")

    return atm


fn = account_creat()
fn(300)
fn(200)
fn(300, False)

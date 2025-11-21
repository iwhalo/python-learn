#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/26 1:02
# @Author  : fuqingyun
# @File    : 03_异常的传递.py
# @Description :

# 定义一个出现异常的方法
def func1():
    print('func1方法开始执行。。。。。')
    num=1/0
    print('func1方法执行结束。。。。。')

# 定义一个无异常的方法，调用上面的方法
def func2():
    print('func2方法开始执行。。。。。')
    func1()
    print('func2方法执行结束。。。。。')

# 定义一个方法，调用上面的方法
def main():
    # func2()
    try:
        func2()
    except Exception as e:
        print(f"出现异常了，异常的信息是：{e}")

main()


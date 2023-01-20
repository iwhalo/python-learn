#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_for循环输出九九乘法表.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/18 14:33 
@Function:
'''


for i in range(1,10):

    for j in range(1,i+1):
        # 内层循环，对其，不换行
        print(f"{j} * {i} = {j * i}\t",end='')

    # 外层循环可以通过print输出一个回车符
    print()
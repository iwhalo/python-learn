#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_函數的參數練習案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/19 17:21 
@Function:
'''


def check(num):
    print("請出示您的健康碼以及72小時核酸證明，並配合測量體溫！")
    if num<=37.5:
        print(f"體溫測量中，您的體溫是：{num}度，體溫正常，請進！")
    else:
        print(f"體溫測量中，你的體溫是：{num}度，需要隔離！")


check(float(input("請輸入您的體溫：")))
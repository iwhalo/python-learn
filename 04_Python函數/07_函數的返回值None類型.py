#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_函數的返回值None類型.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/19 17:46 
@Function:
'''


def say_hi():
    print("你好呀")


result = say_hi()
print(f"無返回值函數，返回的內容是：{result}")
print(f"無返回值函數，返回的類型是：{type(result)}")


def say_hi2():
    print("你好呀")
    return None


result = say_hi2()
print(f"無返回值函數，返回的內容是：{result}")
print(f"無返回值函數，返回的內容類型是：{type(result)}")


# None用於if判斷
def check_age(age):
    if age > 18:
        return "SUCESS"
    else:
        return None


result = check_age(16)
if not result:
    print("未成年人，不可進入")

# None用于声明无初始内容的变量
name = None

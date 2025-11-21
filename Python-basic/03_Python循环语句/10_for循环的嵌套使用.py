#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_for循环的嵌套使用.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/18 14:14 
@Function:
'''
i = 0

for i in range(1, 101):
    print(f"今天是向小美表白的第{i}天，加油坚持。")

    for j in range(1, 11):
        print(f"给小美送的第{j}朵玫瑰花")

    print("小美我喜欢你")

print(f"第{i}天，表白成功")

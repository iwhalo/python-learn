#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_while循环的嵌套应用.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/5 19:21 
@Function:
'''


# 外层：表白100天的控制
# 内层：每天的表白都送10支玫瑰花

i=1

while i<=100:
    print(f"今天是滴{i}天，准备表白...")

    # 内层循环的控制变量
    j=1
    while j<=10:
        print(f"送给小美第{j}支玫瑰花")
        j+=1

    print("小美我喜欢你！")
    i+=1

print(f"坚持到第{i-1}天，表白成功！")
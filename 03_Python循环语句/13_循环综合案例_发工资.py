#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：13_循环综合案例_发工资.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/18 15:47 
@Function:
'''

# 定义账户余额变量
money = 10000

# for循环对员工发工资
for i in range(1, 21):
    import random

    score = random.randint(1, 10)

    if score < 5:
        print(f"员工{i}绩效分{score}，不满足，不发工资，下一位")
        # continue跳过发放
        continue

    # 判断账户余额不足
    if money >= 1000:
        money -= 1000
        print(f"员工{i}，绩效：{score}，满足条件发放工资1000，公司账户余额：{money}")
    else:
        print(f"公司账户余额不足，当前余额：{money}元，不发了，下个月再来")
        # break结束发放
        break




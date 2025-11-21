#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：data_define.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 16:57 
@Function: 数据定义的类
'''


class Record:
    # date=None
    # order_id=None
    # money=None
    # province=None

    def __init__(self, date, order_id, money, province):
        self.date = date  # 订单日期
        self.order_id = order_id  # 订单id
        self.money = money  # 订单金额
        self.province = province  # 销售身份

    #使用str魔术方法输出字符串，否则输出的是对象的地址
    def __str__(self):
        return f"{self.date},{self.order_id},{self.money},{self.province}"
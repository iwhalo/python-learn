#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_一个带有私有成员的类的案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 13:44 
@Function:
'''


class Phone:
    # 私有成员变量
    __is_5g_enable = False

    # 私有成员方法
    def _check_5g(self):
        if self.__is_5g_enable:
            print("5g开启！")
        else:
            print('5g关闭，使用4g网络！')

    # 公开成员方法
    def call_by_5g(self):
        self._check_5g()
        print('正在通话中！')


phone = Phone()
phone.call_by_5g()

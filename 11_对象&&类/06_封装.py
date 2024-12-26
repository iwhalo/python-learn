#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_封装.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 11:46 
@Function: 演示面向对象封装思想中私有成员的使用
'''


# 定义一个类，内含私有成员变量和私有成员方法
class Phone:
    # 私有成员
    __current_voltage = 0.5

    # 私有方法
    def __keep_single_core(self):
        print('让CPU保持单核运行')

    # 类内部的其它方法可以调用私有成员和私有方法
    def call_by_5g(self):
        if self.__current_voltage >= 1:
            print('5g通话已开启！')
        else:
            self.__keep_single_core()
            print('电量不足，无法使用5g通话！')


phone = Phone()
# 类外部无法调用私有成员和私有方法
# phone.__keep_single_core() # AttributeError: 'Phone' object has no attribute '__keep_single_core'. Did you mean: '_Phone__keep_single_core'?
# print(phone.__current_voltage)  # AttributeError: 'Phone' object has no attribute '__current_voltage'. Did you mean: '_Phone__current_voltage'?

phone.call_by_5g()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_Python列表list的循环遍历.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/29 21:47 
@Function:list列表的循环，使用while和for循环两种方式
'''


def list_while_func():
    '''
    使用while循环遍历列表
    :return: None
    '''
    my_list = ["传智教育", "黑马程序员", "Python"]
    # 循环控制变量通过下标索引来控制，默认0
    # 每一次循环将下标索引+1
    # 循环条件：下标索引变量 < 列表的元素数量

    # 定义一个变量用来标记列表的下标
    index = 0  # 下标初始值
    while index < len(my_list):
        # 通过index变量取出对应下标的元素
        element = my_list[index]
        print(f"列表的元素是：{element}")

        # 至关重要，将循环变量(index)每一次循环都+1
        index += 1


def list_for_func():
    '''
    使用for循环遍历列表
    :return: None
    '''
    my_list = [1, 2, 3, 4, 5]
    for element in my_list:
        print(f"列表的元素是：{element}")


list_while_func()

list_for_func()

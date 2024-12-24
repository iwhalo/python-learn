#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_Python集合课后练习.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 16:19 
@Function:
'''

my_list=['黑马程序员','传智播客','黑马程序员','传智播客','itheima','itcast','itheima','itcast','best']

my_set=set()


for ele in my_list:

    my_set.add(ele)


print(my_set)
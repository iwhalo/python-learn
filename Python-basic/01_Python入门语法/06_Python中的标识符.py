#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_Python中的标识符.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/27 19:22 
@Function:
'''

# 规则1：内容限定，限定只能使用：中午、英文、数字、下划线，注意：不能以数字开头
# 1_name="张三"
# name_!="张三"
name_ = "张三"
name_1 = "张三"
_name = "张三"

# 规则2：大小写敏感
Itheima = "黑马程序员"
itheima = 666
print(Itheima)
print(itheima)

# 规则3：不可使用关键字
# class=1
# def=1
Class = 1

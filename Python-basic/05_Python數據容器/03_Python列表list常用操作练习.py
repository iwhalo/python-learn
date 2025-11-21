#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_Python列表list常用操作练习.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/29 21:20 
@Function:
'''

# 1.定义一个列表，并用变量接收它，列表内容是：[21, 25, 21, 23, 22, 20]
my_list = [21, 25, 21, 23, 22, 20]
print(f"定义的列表是：{my_list}")

# 2.追加一个数字31，到列表的尾部
my_list.append(31)
print(f"追加一个元素31后，列表是：{my_list}")

# 3.追加一个新列表[29, 33, 30]，到列表尾部
my_list1=[29,33,30]
my_list.extend(my_list1)
print(f"追加一个新的列表后，列表变成：{my_list}")

# 4.取出第一个元素（应是：21）
num1=my_list[0]
print(f"取出列表的第一个元素是：{num1}，取出第一个元素后的列表是：{my_list}")

# 5.取出最后一个元素（应是：30）
num2=my_list[-1]
print(f"取出列表最后一个元素是：{num2}，取出最后一个元素后的列表是：{my_list}")

# 6.查找元素31，在列表中的下标位置
index=my_list.index(31)
print(f"元素31在列表中的下标索引是：{index}")
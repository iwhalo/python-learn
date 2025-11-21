#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：15_Python数据容器的通用功能.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 17:39 
@Function:
'''

my_list=[1,2,3,4,5]
my_tuple=(1,2,3,4,5)
my_str="abcdefg"
my_set={1,2,3,4,5}
my_dict={"key1":1,"key2":2,"key3":3,"key4":4,"key5":5}

# len元素个数
print(f"列表 元素个数是：{len(my_list)}")
print(f"元组 元素个数是：{len(my_tuple)}")
print(f"字符串 元素个数是：{len(my_str)}")
print(f"集合 元素个数是：{len(my_set)}")
print(f"字典 元素个数是：{len(my_dict)}")
print('===========================================')

# max最大元素
print(f"列表 最大元素是：{max(my_list)}")
print(f"元组 最大元素是：{max(my_tuple)}")
print(f"字符串 最大元素是：{max(my_str)}")
print(f"集合 最大元素是：{max(my_set)}")
print(f"字典 最大元素是：{max(my_dict)}")
print('===========================================')

# min最小元素
print(f"列表 最小元素是：{min(my_list)}")
print(f"元组 最小元素是：{min(my_tuple)}")
print(f"字符串 最小元素是：{min(my_str)}")
print(f"集合 最小元素是：{min(my_set)}")
print(f"字典 最小元素是：{min(my_dict)}")
print('===========================================')

# 类型转换：容器转列表
print(f"列表转列表的结果是：{list(my_list)}")
print(f"元组转列表的结果是：{list(my_tuple)}")
print(f"字符串转列表的结果是：{list(my_str)}")
print(f"集合转列表的结果是：{list(my_set)}")
print(f"字典转列表的结果是：{list(my_dict)}")
print('===========================================')

# 容器转元组
print(f"列表转元组的结果是：{tuple(my_list)}")
print(f"元组转元组的结果是：{tuple(my_tuple)}")
print(f"字符串元组表的结果是：{tuple(my_str)}")
print(f"集合转元组的结果是：{tuple(my_set)}")
print(f"字典转元组的结果是：{tuple(my_dict)}")
print('===========================================')

# 容器转字符串
print(f"列表转字符串的结果是：{str(my_list)}")
print(f"元组转字符串的结果是：{str(my_tuple)}")
print(f"字符串字符串表的结果是：{str(my_str)}")
print(f"集合转字符串的结果是：{str(my_set)}")
print(f"字典转字符串的结果是：{str(my_dict)}")
print('===========================================')

# 容器转集合
print(f"列表转集合的结果是：{set(my_list)}")
print(f"元组转集合的结果是：{set(my_tuple)}")
print(f"字符串集合表的结果是：{set(my_str)}")
print(f"集合转集合的结果是：{set(my_set)}")
print(f"字典转集合的结果是：{set(my_dict)}")
print('===========================================')

# sorted排序，排序的结果是列表
my_list=[76,58,98,37,21]
my_tuple=(367,589,112,532,23)
my_str="yadbczdetfmg"
my_set={365,777,65,879,900}
my_dict={"key9":1,"key7":2,"key8":3,"key3":4,"key1":5}

print(f"列表对象的排序结果是：{sorted(my_list)}")
print(f"元组对象的排序结果是：{sorted(my_tuple)}")
print(f"字符串对象的排序结果是：{sorted(my_str)}")
print(f"集合对象的排序结果是：{sorted(my_set)}")
print(f"字典对象的排序结果是：{sorted(my_dict)}")
print('===========================================')

# 反向排序
print(f"列表对象的排序结果是：{sorted(my_list,reverse=True)}")
print(f"元组对象的排序结果是：{sorted(my_tuple,reverse=True)}")
print(f"字符串对象的排序结果是：{sorted(my_str,reverse=True)}")
print(f"集合对象的排序结果是：{sorted(my_set,reverse=True)}")
print(f"字典对象的排序结果是：{sorted(my_dict,reverse=True)}")
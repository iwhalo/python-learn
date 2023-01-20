#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_Python字符串.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/2/1 19:07 
@Function:
'''

# 通过下标索引取值
my_str="itheima and itcast"

# index方法
value=my_str[2]
value2=my_str[-16]
print(f"从字符串{my_str}中取出小标为2的元素是：{value}，取出下标为-16的元素是：{value2}")

# my_str[2]="H"

num=my_str.index("and")
print(f"从字符串{my_str}中查找and，其起始下标是：{num}")

# replace方法
new_my_str=my_str.replace("it","程序")
print(f"将字符串{my_str}进行替换后得到：{new_my_str}")

# split方法
my_str="hello python itheima itcast"
my_str_list=my_str.split(" ")
print(f"将字符串{my_str}按照空格进行split分割后得到：{my_str_list}，类型是：{type(my_str_list)}")

# strip方法
my_str="  itheima and itcast  "
new_my_str=my_str.strip()
print(f"字符串{my_str}被strip后，结果是：{new_my_str}")

my_str="12itheima and itcast21"
new_my_str=my_str.strip("12")
print(f"字符串{my_str}被strip后，结果是：{new_my_str}")

# 统计字符串中某字符串的出现次数
my_str="itheima and itcast"
count=my_str.count("it")
print(f"字符串{my_str}中it出现的次数是：{count}")

# 统计字符串的长度
num=len(my_str)
print(f"字符串{my_str}的长度是：{num}")
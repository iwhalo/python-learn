#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_函數快速體驗.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/19 14:15 
@Function:
'''

# 需求：統計字符串長度，不使用內置函數

str1="itheima"
str2="itcast"
str3="python"

# 定義一個計數的變量
count=0
for i in str1:
    count+=1
print(f"字符串{str1}的長度是：{count}")

count=0
for i in str2:
    count+=1
print(f"字符串{str2}的長度是：{count}")

count=0
for i in str3:
    count+=1
print(f"字符串{str3}的長度是：{count}")

print('=====================================')

# 可以使用函數來優化這個過程
def my_len(data):
    count=0
    for i in data:
        count+=1
    print(f"字符串{data}的長度是：{count}")

my_len(str1)
my_len(str2)
my_len(str3)
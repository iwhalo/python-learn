#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_Python元组tuple.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/31 20:59 
@Function:
'''

# 定义元组
t1 = (1, "Hello", "True")
t2 = ()
t3 = tuple()
print(f"t1的类型是：{type(t1)}，内容是：{t1}")
print(f"t2的类型是：{type(t2)}，内容是：{t2}")
print(f"t3的类型是：{type(t3)}，内容是：{t3}")

# 定义单个元素的元组
# t4=("hello")  # t4的类型是：<class 'str'>，内容是：hello
t4 = ("hello",)
print(f"t4的类型是：{type(t4)}，内容是：{t4}")

# 元组的嵌套
t5 = ((1, 2, 3), (4, 5, 6))
print(f"t5的类型是：{type(t5)}，内容是：{t5}")

# 下标索引取出内容
num = t5[1][2]
print(f"从嵌套元组中取出的内容是：{num}")

# 元组的操作：index查找方法
t6 = ("传智教育", "黑马程序员", "Python")
index = t6.index("黑马程序员")
print(f"在元组t6中查找 黑马程序员 的下标是：{index}")

# 元组的操作：count统计方法
t7 = ("传智教育", "黑马程序员", "黑马程序员", "黑马程序员", "Python")
num = t7.count("黑马程序员")
print(f"在元组t7中统计黑马程序员的数量有：{num}个")

# 元组的操作：len函数统计元组元素数量
t8 = ("传智教育", "黑马程序员", "黑马程序员", "黑马程序员", "Python")
num = len(t8)
print(f"t8元组中的元素有：{num}个")

# 元组的遍历：while
index = 0
while index < len(t8):
    print(f"元组的元素有：{t8[index]}")
    index += 1

# 元组的遍历：for
for element in t8:
    print(f"元组的元素有：{element}")

# 修改元组内容
# t8[0] = "itcast"    #TypeError: 'tuple' object does not support item assignment
# 定义一个元组，元组中嵌套有list列表，支持对list列表修改
t9=(1,2,["itheima","itcast"])
print(f"t9的内容是：{t9}")
t9[2][0]="黑马程序员"
t9[2][1]="传智教育"
print(f"t9的内容是：{t9}")

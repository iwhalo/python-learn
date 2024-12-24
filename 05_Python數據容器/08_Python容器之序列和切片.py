#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_Python容器之序列和切片.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/2/1 20:18 
@Function:
'''

# 对list进行切片，从1开始，4结束，步长1
my_list=[0,1,2,3,4,5,6]
result1=my_list[1:4]    #步长为1，省略不写；4结束，是不包括4的
print(f"结果1：{result1}") #[1, 2, 3]

# 对tuple进行切片，从头开始，到最后结束，步长1
my_tuple=(0,1,2,3,4,5,6)
result2=my_tuple[:] #起始和结束不写表示从头到尾，步长为1可以省略
print(f"结果2：{result2}")

# 对str进行切片，从头开始，到最后结束，步长2
my_str="01234567"
result3=my_str[::2]
print(f"结果3：{result3}")

# 对str进行切片，从头开始，到最后结束，步长-1
my_str="01234567"
result4=my_str[::-1]    #等同于将序列反转了
print(f"结果4：{result4}")

# 对列表进行切片，从3开始，到1结束，步长-1
my_list=[0,1,2,3,4,5,6]
result5=my_str[3:1:-1]
print(f"结果5：{result5}")

# 对元组进行切片，从头开始，到最后结束，步长-2
my_tuple=(0,1,2,3,4,5,6)
result6=my_tuple[::-2]
print(f"结果6：{result6}")

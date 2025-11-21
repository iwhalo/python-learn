#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_类型注解_变量.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 15:27 
@Function:
'''
import json
from random import random

# 基础数据类型注解
var_1: int = 10
var_2: str = 'itheima'
var_3: bool = True


# 类对象类型注解
class Student:
    pass


stu1: Student = Student()

# 基础容器类型注解
my_list1: list = [1, 2, 3]
my_tuple1: tuple = (1, 2, 3)
my_dict1: dict = {'itheima': 666}

# 容器类型详细注解
my_list2: list[int] = [1, 2, 3]
my_tuple2: tuple[int, str, bool] = (1, 'itheima', True)
my_dict2: dict[str, int] = {'itheima': 666}


# 在注释中进行类型注解
# 除了使用变量：类型，这种语法做注解外，也可以在注释中进行类型注解。
# 语法：
#   type:类型
class Student:
    pass


def func():
    return 10

var_5 = random.randint(1, 10)  # type:int
var_6 = json.loads('{"name":"zhangsan"}')  # type:dict[str,int]
var_7 = func()  # type:int

# 类型注解的限制

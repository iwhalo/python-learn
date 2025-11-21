#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_初识对象.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 10:19 
@Function:
'''


# 设计一个类
class Student:
    name = None
    gender = None
    nationality = None
    native_place = None
    age = None


# 创建一个对象
stu_1 = Student()

# 对象属性赋值
stu_1.name = 'zhangsan'
stu_1.gender = '男'
stu_1.nationality = '中国'
stu_1.native_place = '山东省'
stu_1.age = 18

# 获取对象中记录的信息
print(stu_1)    # <__main__.Student object at 0x00000197BBEE4DD0>
print(stu_1.name)

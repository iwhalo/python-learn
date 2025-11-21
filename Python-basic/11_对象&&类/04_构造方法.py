#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_构造方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 11:01 
@Function: 演示使用构造方法对成员变量进行赋值
'''


# 构造方法的名称：__init__

class Student:
    name = None
    age = None
    tel = None

    def __init__(self, name, age, tel):
        self.name = name
        self.age = age
        self.tel = tel
        print('Student类创建了一个对象')


stu = Student('周杰伦', 18, '123456789')
print(stu.name)
print(stu.age)
print(stu.tel)
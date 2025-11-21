#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_其它内置方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 11:14 
@Function:
'''


# __init__方法
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student('周杰伦', 30)
print(stu)  # <__main__.Student object at 0x00000162EF1C4D10>
print(str(stu))  # <__main__.Student object at 0x00000162EF1C4D10>
print('=========================================================')


# __str__魔术方法
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __str__魔术方法
    def __str__(self):
        return f"Student类对象，name：{self.name}，age：{self.age}"


stu = Student('周杰伦', 30)
print(stu)  # Student类对象，name：周杰伦，age：30
print(str(stu))  # Student类对象，name：周杰伦，age：30
print('==============================================================')


# __lt__ 小于符号比较方法
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __lt__ 小于符号比较方法
    def __lt__(self, other):
        return self.age < other.age


stu1 = Student('周杰伦', 30)
stu2 = Student('林俊杰', 15)
print(stu1 < stu2)  # False
print(stu1 > stu2)  # True
print('==============================================================')


# __le__ 小于等于比较符号方法
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __le__ 小于等于符号比较方法
    def __le__(self, other):
        return self.age <= other.age


stu1 = Student('周杰伦', 30)
stu2 = Student('林俊杰', 50)
print(stu1 >= stu2)
print(stu1 <= stu2)
print('=================================================================')


# __eq__ 比较运算符
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __eq__比较运算符
    def __eq__(self, other):
        return self.age == other.age


stu1 = Student('周杰伦', 18)
stu2 = Student('林俊杰', 19)
print(stu1 == stu2)

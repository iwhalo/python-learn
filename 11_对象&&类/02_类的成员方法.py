#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：02_类的成员方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 10:33 
@Function:
'''

# 定义一个带有成员方法的类
class Student:
    name=None

    def say_hi(self):
        print(f"大家好，我是{self.name}")

    def say_hi2(self,msg):
        print(f"大家好，我是{self.name},{msg}")

stu=Student()
stu.name='zhangsan'
stu.say_hi()

stu2=Student()
stu2.name='林俊杰'
stu2.say_hi2('你们好吗')



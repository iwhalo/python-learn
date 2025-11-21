#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_工厂模式.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 11:19 
@Function: 演示设计模式之工厂模式
'''


class Person:
    pass


class Worker(Person):
    pass


class Student(Person):
    pass


class Teacher(Person):
    pass


class PersonFactory:
    def get_person(self, p_type):
        if p_type == 'w':
            return Worker()
        elif p_type == 's':
            return Student()
        else:
            return Teacher()


pf = PersonFactory()
worker = pf.get_person('w')
student = pf.get_person('s')
teacher = pf.get_person('t')

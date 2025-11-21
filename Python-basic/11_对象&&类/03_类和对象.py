#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_类和对象.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 10:50 
@Function:
'''

# 设计一个闹钟类
class Clock:
    id=None
    price=None

    def ring(self):
        import winsound
        winsound.Beep(2000,3000)


# 构建2个闹钟对象并让其工作
clock1=Clock()
clock1.id='003032'
clock1.price=19.99
print(f'闹钟ID：{clock1.id},价格：{clock1.price}')
clock1.ring()

clock2=Clock()
clock2.id='003033'
clock2.price=29.99
print(f'闹钟ID：{clock2.id},价格：{clock2.price}')
clock2.ring()
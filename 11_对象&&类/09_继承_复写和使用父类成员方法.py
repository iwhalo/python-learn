#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_继承_复写和使用父类成员方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 15:00 
@Function:
'''


# 父类
class Phone:
    IMEI = None
    producer = 'ITCAST'

    def call_by_5g(self):
        print('使用5g网络进行通话！')


# 定义子类，复写父类成员
class MyPhone(Phone):
    producer = 'ITHEIMA'  # 复写父类的成员属性

    def call_by_5g(self):
        print('开启CPU单核模式，确保通话的时候省电')
        # print('使用5g网络进行通话')

        # 调用父类
        # 方法1
        print(f"父类的厂商是：{Phone.producer}")
        Phone.call_by_5g(self)

        # 方法2
        print(f"父类的厂商是：{super().producer}")
        super().call_by_5g()

        print('关闭CPU单核模式，确保性能')


phone = MyPhone()
print(phone.producer)
phone.call_by_5g()

# 在子类中，调用父类成员
'''
调用父类同名成员:
    一旦复写父类成员，那么类对象调用成员的时候，就会调用复写后的新成员
    如果需要使用被复写的父类的成员，需要特殊的调用方式：
        方式1：
        ·调用父类成员
            使用成员变量：父类名成员变量
            使用成员方法：父类名.成员方法(self)
        方式2：
        ·使用super(0调用父类成员
            使用成员变量：super()成员变量
            使用成员方法：super().成员方法()
'''
# 方法1
print()

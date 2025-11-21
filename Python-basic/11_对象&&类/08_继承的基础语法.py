#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_继承的基础语法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 14:07 
@Function: 演示面向对象：继承的基础语法
'''


# 演示单继承

# 父类
class Phone:
    IMEI = None
    producer = 'HW'

    def call_by_4g(self):
        print('4g通话！')


# 子类继承父类
class Phone2022(Phone):
    face_id = '10001'

    def call_by_5g(self):
        print('2022年新功能，5g通话！')


phone = Phone()
phone.IMEI = 88899
print(phone.producer)
phone.call_by_4g()

print('==========================')

phone2022 = Phone2022()
phone2022.IMEI = 12345
print(phone2022.producer)
phone2022.call_by_4g()

print(phone2022.face_id)
phone2022.call_by_5g()
print('===================================')


# 演示多继承

class NFCReader:
    nfc_type = '第五代'
    producer = '小米'

    def read_card(self):
        print('NFC读卡功能')

    def write_card(self):
        print('NFC写卡功能')


class Remote_Control:
    rc_type = '红外遥控'

    def rc_control(self):
        print('红外遥控开启了')


# 多个父类中，如果有同名的成员(比如父类Phone和NFCReader中都有成员producer)，那么默认以继承顺序（从左到右)为优先级。
# 即：先继承的保留，后继承的被覆盖
class MyPhone(Phone, NFCReader, Remote_Control):
    # 子类继承父类后不再添加新变量和方法
    pass


myPhone = MyPhone()
myPhone.IMEI = 112233
print(myPhone.IMEI)
print(myPhone.producer)
myPhone.call_by_4g()
print(myPhone.nfc_type)
myPhone.read_card()
myPhone.write_card()
print(myPhone.rc_type)
myPhone.rc_control()

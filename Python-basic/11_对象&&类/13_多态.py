#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：13_多态.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 16:19 
@Function:
'''

class Animal:
    def speek(self):
        pass

class Dog(Animal):
    def speek(self):
        print('汪汪汪......')

class Cat(Animal):
    def speek(self):
        print('喵喵喵......')

def make_noise(animal:Animal):
    animal.speek()

# 演示多态
dog=Dog()
cat=Cat()

make_noise(dog)
make_noise(cat)


# 演示抽象类
# 抽象类
class AC:
    # 抽象方法：没有具体实现的方法
    def cool_wind(self):
        '''制冷'''
        pass

    def hot_wind(self):
        '''制热'''
        pass

    def swing_l_(self):
        '''左右摆风'''
        pass

# 子类重写父类的成员方法
class Midea_AC(AC):
    def cool_wind(self):
        print('美的空调制冷！')
    def hot_wind(self):
        print('美的空调制热！')
    def swing_l_(self):
        print('美的空调左右摆风！')

class Gree_AC(AC):
    def cool_wind(self):
        print('格力空调制冷！')
    def hot_wind(self):
        print('格力空调制热')
    def swing_l_(self):
        print('格力空调左右摆风')

def make_cool(ac:AC):
    ac.cool_wind()

def make_hot(ac:AC):
    ac.hot_wind()

def make_swing(ac:AC):
    ac.swing_l_()

midea_ac=Midea_AC()
gree_ac=Gree_AC()
make_cool(midea_ac)
make_hot(midea_ac)
make_swing(midea_ac)

make_cool(gree_ac)
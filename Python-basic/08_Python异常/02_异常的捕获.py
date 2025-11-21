#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/26 0:37
# @Author  : fuqingyun
# @File    : 02_异常的捕获.py
# @Description :

# 异常的基本捕获语法
try:
    f=open('D:/abc.txt','r',encoding='UTF-8')
except:
    print('出现异常了，因为文件不存在，我将open的模式改为W')
    f=open('D:/abc.txt','w',encoding='UTF-8')

# 捕获指定异常
# 1/0 # ZeroDivisionError: division by zero
# print(name) # NameError: name 'name' is not defined

try:
    print(name)
    # 1/0
except NameError as e:
    print('出现了变量未定义的异常！')
    print(e)    # NameError: name 'name' is not defined

print('====================================')

# 捕获多个异常
# 当捕获多个异常时，可以把要捕获的异常类型的名字，放到except后，并使用元组的方式进行书写。
try:
    # print(name)
    1/0
except (NameError,ZeroDivisionError) as e:
    print('出现了变量未定义的异常 或者 除以0的异常')
    print(e)

print('==================================')

# 未正确设置捕获异常类型，将无法捕获异常


# 捕获所有异常
try:
    # f=open('D:/aaaa.txt','r',encoding='UTF-8')
    print('hello')
except Exception as e:
    print('出现异常了')
else:
    print('好高兴，没有异常！')

print('====================================')

# 异常的finally
try:
    f=open('D:/1235.txt','r',encoding='UTF-8')
except Exception as e:
    print('出现异常了！')
    f=open('D:/1235.txt','w',encoding='UTF-8')
else:
    print('好高兴，没有异常')
finally:
    print('我是finally，有没有异常，我都要执行！')
    f.close()


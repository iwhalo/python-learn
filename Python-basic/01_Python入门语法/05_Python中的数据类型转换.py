#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_Python中的数据类型转换.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/26 21:24 
@Function:
'''


print('hello world')

name='zhangsan'
print(name)

# input
userName=input('请输入用户名：')  # 阻塞
print('您输入的用户名是：'+userName)
print(type(userName))   # <class 'str'>

money=input('请输入缴费金额：')
print('您输入的缴费金额是：'+money)
print(type(money))  # <class 'str'>

# print(money+1000)   # TypeError: can only concatenate str (not "int") to str
print(float(money)+1000)    # 1013.14
print(money+str(1000))      # 13.141000

a=input('请输入数字a：')
b=input('请输入数字b：')

# 拼接
print(a+b)

# 计算9.9+3.3
# print(int(a)+int(b))    #ValueError: invalid literal for int() with base 10: '9.9'
# 输入的9.9是字符串且带有小数点，无法直接转换为int类型
print(int(float(a))+int(float(b)))  # 5
print(float(a)+float(b))    # 5.5

# bool---------->int
print(int(True))
print(int(False))

print(float(True))
print(float(False))

print(str(True))
print(str(False))

a=2
print(bool(a))
b=1
print(bool(b))

c=0
print(bool(c))


print('==================================================')
#将数字类型转换成字符串
num_str=str(11)
print(type(num_str),num_str)    # <class 'str'> 11

float_str=str(13.14)
print(type(float_str),float_str)    # <class 'str'> 13.14


#将字符串转换成数字
num=int("11")
print(type(num),num)    # <class 'int'> 11
num2=float("13.14")
print(type(num2),num2)  # <class 'float'> 13.14

# num3=int("黑马程序员")
# print(type(num3),num3)


#整数转浮点数
float_num=float(11)
print(type(float_num),float_num)

#浮点数转整数
int_num =int(13.14)
print(type(int_num),int_num)
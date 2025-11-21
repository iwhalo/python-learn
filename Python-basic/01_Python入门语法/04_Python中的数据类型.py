#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_Python中的数据类型.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/26 21:13 
@Function:
'''


'''
数据类型：
    numbers：
        int     有符号整型
        long    长整型（也可以代表八进制和十六进制）
        float   浮点型
        complex 复数
        
    布尔类型：
        True
        False
        
    字符串：
        String
        
    列表：
        List
        
    元组：
        Tuple
        
    字典：
        Dictionary
        
'''
money=28    # <class 'int'>
print(type(money))

height=1.79     # <class 'float'>
print(type(height))

name='zhangsan'     # <class 'str'>
print(type(name))

message="李白说：'飞流直下三千尺'"
print(message)

msg="" \
    " 静夜思\n" \
    "床前明月光，\n" \
    "疑是地上霜。\n" \
    "举头望明月，\n" \
    "低头思故乡。\n"

msg1='''
    静夜思
     李白
床前明月光，疑是地上霜。
举头望明月，低头思故乡。
'''
print(msg1)

# 布尔类型：True False
isLogin=True    # <class 'bool'>
print(isLogin)  # True
print(type(isLogin))

isLogin=False   # <class 'bool'>
print(isLogin)  # False
print(type(isLogin))

print('==================================================================================================')

# 使用print直接输出类型信息
print(type("黑马程序员"))
print(type(666))
print(type(13.14))
# 使用变量存储type()语句的结果
string_type = type("黑马程序员")
int_type = type(666)
float_type = type(13.14)
print(string_type)
print(int_type)
print(float_type)
# 使用type()语句，查看变量中存储的数据类型信息
name = "黑马程序员"
name_type = type(name)
print(name_type)

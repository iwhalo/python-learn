#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_Python中的字符串的多种定义方式.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/27 20:52 
@Function:
'''

"""
-   单引号定义方法
-   双引号定义方法
-   三引号定义方法
"""

# 单引号定义方法，使用单引号进行包围
name = '黑马程序员'
print(type(name))

# 双引号定义方法
name = "黑马程序员"
print(type(name))

# 三引号定义方法，写法和多行注释一样
name = """
我是
黑马
程序员
"""
print(type(name))

# 在单引号字符串内包含双引号
name = '"黑马程序员"'
print(name)
# 在双引号字符串内包含单引号
name = "'黑马程序员'"
print(name)
# 使用转义字符 \ 解除引号的效用
name = "\"黑马程序员\""
print(name)
name = '\'黑马程序员\''
print(name)

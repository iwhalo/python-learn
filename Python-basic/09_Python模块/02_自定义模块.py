#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：02_自定义模块.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 10:14 
@Function:
'''

# 导入自定义模块使用
# import my_moudle1
# my_moudle1.test(1,2)

# 导入不同模块的同名功能
# from my_moudle1 import test
# from my_moudle2 import test
# 注意事项：当导入多个模块的时候，且模块内有同名功能，当调用这个功能的时候，调用到的是后面导入的模块的项能
# test(6,6)

# __main__变量
from my_moudle1 import test

print('===========================')

# __all__变量
from my_moudle1 import *
test_a(1,2)
# test_b(1,2)

from my_moudle1 import test_b
test_b(1,2)
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_包.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 10:56 
@Function:
'''

# import my_package.my_moudle1
# import my_package.my_moudle2
#
# my_package.my_moudle1.info_print1()
# my_package.my_moudle2.info_print2()
#
#
#
# from my_package import my_moudle1
# from my_package import my_moudle2
# my_moudle1.info_print1()
# my_moudle2.info_print2()
#
#
# from my_package.my_moudle1 import info_print1
# from my_package.my_moudle2 import info_print2
# info_print1()
# info_print2()

from my_package import *
my_moudle1.info_print1()
my_moudle2.info_print2()
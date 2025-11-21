#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：my_moudle.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 10:15 
@Function:
'''

def test(a,b):
    print(a+b)

print('==========模块内调用开始============')
test(5,5)
print('==========模块内调用结束============')

# 模块内调用的时候name变量==main，if为true，执行该调用
# 模块外调用的时候，name变量！=main，if为False，不会执行该调用
if __name__ == '__main__':
    test(3,4)

__all__=['test_a']

def test_a(a,b):
    print(a+b)

def test_b(a,b):
    print(a-b)

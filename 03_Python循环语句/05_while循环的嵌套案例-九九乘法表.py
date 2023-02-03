#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_while循环的嵌套案例-九九乘法表.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/5 19:31 
@Function:
'''

print('helloworld')
print('hello\tworld')

i=1
while i<=9:
    j=1
    while j<=i:
        print(f"{j} * {i} = {j*i}\t",end="")    # 通过\t制表符进行对齐；end=""可输出不换行
        j+=1

    i+=1
    print()  #print空内容就是输出一个换行
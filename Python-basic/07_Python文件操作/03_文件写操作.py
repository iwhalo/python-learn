#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_文件写操作.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 21:12 
@Function:
'''
import time

# # 打开文件，不存在的文件
# f=open('../notes/test.txt','w',encoding='UTF-8')
# # write写入
# f.write("Hello World!") # 内容写入到内存中
#
# # time.sleep(1000)
#
# # flush刷新
# f.flush()   # 将内存中积攒的内容写入到文件中
# time.sleep(1000)
#
# # close关闭
# f.close()

# 打开一个存在的文件
f=open('../../notes/test.txt', 'w', encoding='UTF-8')

# write写入，flush刷新
f.write("黑马程序员")

# close关闭
f.close()


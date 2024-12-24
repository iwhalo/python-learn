#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_文件追加写入.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 21:21 
@Function:
'''

# f=open('../notes/test1.txt','a',encoding='UTF-8')
# f.write("itcast")
# f.flush()
# f.close()

f=open('../notes/test1.txt','a',encoding='UTF-8')
f.write("\nitcast传智播客")
f.close()
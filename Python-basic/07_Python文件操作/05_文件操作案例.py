#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_文件操作案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 21:29 
@Function:
'''

# 打开文件得到文件对象，准备读取
fr=open('../notes/test2.txt','r',encoding='UTF-8')

# 打开文件得到文件对象，准备写入
fw=open('../notes/test3.txt','w',encoding='UTF-8')

# for循环读取文件
for line in fr:
    line=line.strip()
    # 判断内容，将满足的内容写入
    if line.split(',')[4]=='测试':
        continue
    fw.write(line)
    # 由于前面对内容进行了strip操作，所以这一步要将换行符加回来
    fw.write('\n')

# fw.flush()

# close两个文件对象
fr.close()
fw.close()  # 写出文件调用close()会自动flush()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：02_统计文本中单词数量.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 20:58 
@Function:
'''

f = open('../../notes/note.md', 'r', encoding='UTF-8')
content = f.read()

count = content.count('img')

print(count)

# 一行行读取
f = open('../../notes/note.md', 'r', encoding='UTF-8')
count1 = 0
for line in f:
    # line=line.replace('\n','')
    line = line.strip()
    words = line.split(" ")

    print(words)

    for word in words:
        if word == "img":
            count1 += 1

print(count1)

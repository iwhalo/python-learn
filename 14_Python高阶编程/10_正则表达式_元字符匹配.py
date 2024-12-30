#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_正则表达式_元字符匹配.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 19:58 
@Function: 演示Python正则表达式使用元字符进行匹配
'''

import re

s = "itheima1 @@python2 !!666 ##itcast3"

result = re.findall("\d", s)  # 字符串前面带上r的标记，表示字符串中转义字符无效，就是普通字符的意思
print(result)

# 找出特殊字符
result = re.findall(r'\W', s)
print(result)

# 找出全部英文字母
result = re.findall(r'[a-zA-Z]', s)
print(result)

# 匹配账号，只能由字母或数字组成，长度限制6到10位
r = '^[0-9a-zA-Z]{6,10}$'  # 正则里面不要有空格
s = "1234567Ab_"
print(re.findall(r, s))

# 匹配QQ号，要求纯数字，长度5-11，第一位不为0
r = '^[1,9][0-9]{4,10}$'  # 不加^和$的话，匹配的是局部字符串，能匹配上就返回，加了的话就会从开头匹配到结尾
s = '12345678'
print(re.findall(r, s))

# 匹配邮箱地址，只允许QQ、163、Gmail这三种邮箱地址
r = r'(^[\w-]+(\.[\w-]+)*@(qq|163|gmail)(\.[\w-]+)+$)'
s = 'a.b.c.d.e.f.g@qq.com.a.b.c.d.e'
print(re.match(r, s))
print(re.findall(r, s))

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：01_json数据格式.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 14:12 
@Function:
'''
import json
# 准备列表，列表内每一个元素都是字典，将其转换为json
data=[{"name":"张大山","age":11},{"name":"王大锤","age":12},{"name":"赵晓辉","age":15}]
json_str=json.dumps(data,ensure_ascii=False)
print(type(json_str))
print(json_str)

# 准备字典，将字典转换为json
d={"name":"周杰伦","addr":"台北"}
json_str=json.dumps(d,ensure_ascii=False)
print(type(json_str))
print(json_str)

# 将json字符串转换为Python数据类型[{k:v,k:v},{k:v,k:v}]
str='[{"name": "张大山", "age": 11}, {"name": "王大锤", "age": 12}, {"name": "赵晓辉", "age": 15}]'
l=json.loads(str)
print(type(l))
print(l)

# 将json字符串转换为Python数据类型{k:v,k:v}
s='{"name":"周杰伦","addr":"台北"}'
d=json.loads(s)
print(type(d))
print(d)
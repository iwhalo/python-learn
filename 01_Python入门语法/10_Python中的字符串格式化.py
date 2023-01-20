#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_Python中的字符串格式化.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/27 21:12 
@Function:
'''

# 通过占位的形式，完成拼接
name = "黑马程序员"
message = "学IT来：%s" % name
print(message)

# 通过占位的形式，完成数字和字符串的拼接
class_num = 57
avg_salary = 20000
message = "Python大数据科学，北京%s期，毕业平均工资：%s" % (class_num, avg_salary)
print(message)

name = "传智播客"
setup_year = 2006
stock_price = 19.99
message = "%s，成立于：%d，我今天的股价是：%f。" % (name, setup_year, stock_price)
print(message)
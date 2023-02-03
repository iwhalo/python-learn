#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_Python中的变量.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2022/12/26 20:24 
@Function: Python中的变量
'''

'''
变量：'容器'
弱语言：变量声明的时候对数据类型不是很严格
java:   int a=100
        float b=9.9
        
python： a=100
格式：变量名=值

变量名的命名规范：
1、字母，数字，下划线，不能以数字开头
2、严格区分大小写
3、不能使用关键字
'''

name='zhangsan'
age=19

a1=100
# a+=200
# a$=200
a_=200
# a$b=123


# 命名规则
# 见名知意
# 驼峰命名法：
# 小驼峰：开头第一个单词全部小写，getNameByLine
getNameByLine='hello'

get_name_by_line='hello'

# 大驼峰：Python面向对象：类名   每一个单词的首字母都采用大写
GetNameByLine='hello'

# 关键字


名字='zhnagsan'
print(名字)


# 定义一个变量，用来记录钱包余额
money = 50
# 通过print语句，输出变量记录的内容
print("钱包还有：", money)

# 买了一个冰淇淋，花费10元
money=money-10
print("买了冰淇淋花费10元，还剩：", money, "元")

# 假设，每隔一小时，输出一下钱包余额
print("现在是下午1点，钱包余额剩余：", money)
print("现在是下午2点，钱包余额剩余：", money)
print("现在是下午3点，钱包余额剩余：", money)
print("现在是下午4点，钱包余额剩余：", money)

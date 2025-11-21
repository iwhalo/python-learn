#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：12_Python字典.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 16:29 
@Function:
'''

# 定义字典
my_dict1={"王力宏":99,"周杰伦":88,"林俊杰":77}

# 定义空字典
my_dict2={}
my_dict3=dict()

print(f"字典1的内容是：{my_dict1}，类型是：{type(my_dict1)}")
print(f"字典2的内容是：{my_dict2}，类型是：{type(my_dict2)}")
print(f"字典2的内容是：{my_dict3}，类型是：{type(my_dict3)}")

# 定义重复字典
my_dict1={"王力宏":99,"周杰伦":88,"林俊杰":77}
my_dict1={"王力宏":88,"周杰伦":88,"林俊杰":77}
print(f"重复key的字典内容是：{my_dict1}")

# 字典数据的获取
my_dict1={"王力宏":99,"周杰伦":88,"林俊杰":77}
score=my_dict1["王力宏"]
print(f"王力宏的考试分数是：{score}")

# 字典的嵌套
stu_score_dict={
    "王力宏":{
        "语文":77,
        "数学":66,
        "英语":33
    },
    "周杰伦":{
        "语文":88,
        "数学":86,
        "英语":55
    },
    "林俊杰":{
        "语文":99,
        "数学":96,
        "英语":66
    }
}

print(f"学生的考试信息时：{stu_score_dict}")

# 从嵌套字典中获取数据
# 看一下周杰伦的语文信息
score=stu_score_dict["周杰伦"]["语文"]
print(f"周杰伦的语文信息时：{score}")




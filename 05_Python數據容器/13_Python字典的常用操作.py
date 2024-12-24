#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：13_Python字典的常用操作.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 16:53 
@Function:
'''

# 定义字典
my_dict={"王力宏":99,"周杰伦":88,"林俊杰":77}

# 新增元素
my_dict["张信哲"]=66
print(f"新增元素后的字典内容是：{my_dict}")

# 更新元素
my_dict["王力宏"]=33
print(f"更新元素后的字典内容是：{my_dict}")

# 删除元素
score=my_dict.pop("王力宏")
print(f"字典中被删除一个元素后变成：{my_dict}，\n王力宏的考试分数是：{score}")

# 清空元素
my_dict.clear()
print(f"字典被清空后变成：{my_dict}")

# 获取全部的key
my_dict={"王力宏":99,"周杰伦":88,"林俊杰":77}
keys=my_dict.keys()
print(f"字典的全部key是：{keys}")

# 遍历字典
# 方式1：通过获取到全部key来完成遍历
for key in keys:
    print(f"字典的key是：{key}")
    print(f"字典\"{key}\"的value是：{my_dict[key]}")
# 方式2：直接对字典进行for循环，每一次循环都是直接得到key
for key in my_dict:
    print(f"2字典的key是：{key}")
    print(f"2字典\"{key}\"的value是：{my_dict[key]}")

# 统计字典内的元素数量,len()函数
num=len(my_dict)
print(f"字典中的元素数量有{num}个")

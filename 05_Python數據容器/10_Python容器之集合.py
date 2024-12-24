#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_Python容器之集合.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/4/25 19:44 
@Function:
'''

# 定义集合
my_set={'传智教育','黑马程序员','itheima','传智教育','黑马程序员','itheima','传智教育','黑马程序员','itheima'}
my_set_empty=set()  # 定义空集合

print(f"my_set的内容是：{my_set}，类型是{type(my_set)}")
print(f"my_set_empty的内容是：{my_set_empty}，类型是{type(my_set_empty)}")

# 添加新元素
my_set.add("python")
my_set.add("传智教育")
print(f"my_set添加元素后的结果是：{my_set}")

# 移除元素
my_set.remove("黑马程序员")
print(f"my_set移除 黑马程序员 之后的结果是：{my_set}")

# 随机取出一个元素
my_set={"传智教育","黑马程序员","itheima"}
element=my_set.pop()
print(f"集合被取出元素是：{element}，取出元素后的集合是：{my_set}")

# 清空集合
my_set.clear()
print(f"集合被清空，结果是：{my_set}")

# 取2个集合的差集
set1={1,2,3}
set2={1,4,5}
set3=set1.difference(set2)
print(f"取出差集后的结果是：{set3}")
print(f"取出差集后，原有set1的内容是：{set1}")
print(f"取出差集后，原有set2的内容是：{set2}")

# 消除两个集合的差集
set1={1,2,3}
set2={1,4,5}
set1.difference_update(set2)
print(f"消除差集后，集合1的结果是：{set1}")
print(f"消除差集后，集合2的结果是：{set2}")

# 两个集合合并为一个
set1={1,2,3}
set2={1,4,5}
set3=set1.union(set2)
print(f"两个集合合并后的结果是：{set3}")
print(f"两个集合合并后，原有集合set1的内容是：{set1}")
print(f"两个集合合并后，原有集合set2的内容是：{set2}")

# 统计集合元素数量
set1={1,2,3,4,5,1,2,3,4,5}
num=len(set1)
print(f"集合内的元素数量有：{num}")

# 集合的遍历
# 集合不支持下标索引，不能用while循环
# 可以用for循环
set1={1,2,3,4,5}
for i in set1:
    print(f"集合set1的元素有：{i}")
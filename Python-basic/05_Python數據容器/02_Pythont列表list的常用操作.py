#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：02_Pythont列表list的常用操作.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/28 21:13 
@Function:
'''
my_list = ["itcast", "itheima", "python"]
# 1.1 查找某元素在列表内的下标索引
index = my_list.index("itheima")
print(f"itheima在列表中的下标索引值是：{index}")

# 1.2 如果被查找的元素不存在，会报错
# index=my_list.index("hello")
# print(f"hello在列表中的下标索引值是：{index}")

# 2. 修改特定下标索引值
my_list[0] = "传智教育"
print(f"列表被修改元素值后，结果是：{my_list}")

# 3. 在指定下标位置插入新元素
my_list.insert(1, "best")
print(f"列表插入元素后，结果是：{my_list}")

# 4. 在列表的尾部追加‘’单个‘’新元素
my_list.append("douyu")
print(f"列表追加单个元素后，结果是：{my_list}")

# 5. 在列表的尾部追加‘’一批‘’新元素
my_list2 = [1, 2, 3]
my_list.extend(my_list2)
print(f"列表再追加了一个新的元素后，结果是：{my_list}")

# 6. 删除指定下标索引的元素（2种方式）
my_list = ["itcast", "itheima", "python"]
# 6.1 方式1：del 列表[下标]
del my_list[2]
print(f"列表删除指定下标元素后，结果是：{my_list}")

# 6.2 方式2：列表.pop(下标)
my_list = ["itcast", "itheima", "python"]
element=my_list.pop(2)
print(f"通过pop方法取出元素后列表内容是：{my_list}，取出的元素是：{element}")

# 7 删除某元素在列表中的第一个匹配项
my_list = ["itcast", "itheima","itcast", "itheima", "python"]
my_list.remove("itheima")
print(f"通过remove方法移除元素后，列表的结果是：{my_list}")

# 8. 清空列表内容
my_list.clear()
print(f"列表被清空了，结果是：{my_list}")

# 9. 统计某元素在列表内的数量
my_list = ["itcast", "itheima","itcast", "itheima", "python"]
num=my_list.count("itheima")
print(f"列表内itheima的数量是：{num}")

# 10. 统计列表内的元素数量
my_list = ["itcast", "itheima","itcast", "itheima", "python"]
num=len(my_list)
print(f"列表内的元素数量有 {num} 个")
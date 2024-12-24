#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：14_Python字典课后练习.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/25 17:12 
@Function:
'''

user_dict = {
    "王力宏": {
        "部门": "科技部",
        "工资": 3000,
        "级别": 1
    },
    "周杰伦": {
        "部门": "市场部",
        "工资": 5000,
        "级别": 2
    },
    "林俊杰": {
        "部门": "市场部",
        "工资": 7000,
        "级别": 3
    },
    "张学友": {
        "部门": "科技部",
        "工资": 4000,
        "级别": 1
    },
    "刘德华": {
        "部门": "市场部",
        "工资": 6000,
        "级别": 2
    }
}
print(f"全体员工当前信息如下：\n{user_dict}")

print(f"对所有级别为1的员工，级别上升1级，薪水增加1000元")

for key in user_dict:
    if user_dict[key]['级别'] == 1:
        user_dict[key]["级别"] += 1
        user_dict[key]["工资"] += 1000
print(f"调级调薪后当前全体员工的信息如下：\n{user_dict}")

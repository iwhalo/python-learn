#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：2023年日历.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/4/6 14:08 
@Function:
'''
import calendar

# 创建一个 Calendar 对象
cal = calendar.Calendar()

# 打印每个月份的日历表
for month in range(1, 13):
    # 获取该月份的日历表
    month_cal = cal.monthdayscalendar(2024, month)

    # 打印月份和星期几标头
    print('\n{0} {1}\n'.format(calendar.month_name[month], 2023))
    print('Mo Tu We Th Fr Sa Su')

    # 遍历并打印日历表中的每一行
    for week in month_cal:
        # 将每个单元格填充为两个字符的宽度并用空格填充任何空位
        week_str = ' '.join([str(day).rjust(2) if day != 0 else '  ' for day in week])

        # 打印整行
        print(week_str)

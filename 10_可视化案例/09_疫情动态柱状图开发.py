#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_疫情动态柱状图开发.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 19:48 
@Function:
'''

from pyecharts.charts import Bar,Timeline
from pyecharts.options import LabelOpts

# 读取数据
f = open('full_data.csv', 'r', encoding='UTF-8')
content_list = f.readlines()
# print(content_list)

# 关闭文件
f.close()

# 删除第一条数据
content_list.pop(0)

# print(content_list)

# dates_Asia = []
# users_Asia = []
#
# for element in content_list:
#     # print(element)
#     # print(type(element))
#     ele = element.split(',')
#     # print(ele)
#     # print(ele[0])
#     if ele[1]=='Asia':
#         dates_Asia.append(ele[0])
#         users_Asia.append(ele[4])
#
# print(dates_Asia)
# print(users_Asia)

# 组装数据

# 将数据转为字典存储，格式为：
# {日期：[[区域，确诊人数],[区域，确诊人数],[区域，确诊人数],......],日期：[[区域，确诊人数],[区域，确诊人数],[区域，确诊人数],......],......}
# {2020-01-05：[[Afghanistan，0],[Angola，1],[Asia，2],......],2020-01-06：[[Afghanistan，0],[Angola，1],[Asia，2],......],......}
# 定义一个字典

def data_create(date_str):
    dates = []
    users = []
    geos = set()
    for element in content_list:
        # print(element)
        # print(type(element))
        ele = element.split(',')
        # print(ele)
        # print(ele[0])
        # print(ele[1])
        # if ele[1] == str:
        #     dates.append(ele[0])
        #     users.append(ele[4])

        # dates.append(ele[0])
        if ele[0] == date_str:
            geos.add(ele[1])
            users.append(ele[4])

    # print(dates)
    # print(users)
    return geos, users
    f.close()


# bar1 = Bar()
# bar1.add_xaxis(dates)
# bar1.add_yaxis('每日确诊人数', users, label_opts=LabelOpts(position='right'))
# bar1.reversal_axis()

# bar1.render('疫情动态数据.html')

# 创建柱状图
def bar_create(geos, users):
    bar = Bar()
    bar.add_xaxis(list(geos))
    bar.add_yaxis('每日确诊人数', users, label_opts=LabelOpts(position='right'))
    bar.reversal_axis()
    return bar


# dates, geos, users = data_create()
# print(dates)
# print(geos)
# print(users)


# bar=bar_create(dates,geos,users)

# timeline = Timeline()
#
# for element in content_list:
#     ele = element.split(',')
#     print(ele[0])
#     for date in ele[0]:
#         geos, users = data_create(date)
#         bar=bar_create(geos,users)
#         timeline.add(bar,ele[0])
#
# timeline.render('疫情动态数据.html')

# timeline = Timeline()
# timeline.add(bar, 'Asia数据')
# timeline.add(bar_Aruba, 'Aruba数据')
# timeline.add(bar_Europe, 'Europe数据')

# timeline.render('疫情动态数据.html')

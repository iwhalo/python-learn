#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_疫情数据可视化.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 21:53 
@Function:
'''

from pyecharts.charts import Bar,Timeline
from pyecharts.options import LabelOpts,TitleOpts
from pyecharts.globals import ThemeType

# 读取数据
f = open('full_data.csv', 'r', encoding='UTF-8')
content_list = f.readlines()
# print(content_list)

# 关闭文件
f.close()

# 删除第一条数据
content_list.pop(0)
# print(content_list)

# 将数据转为字典存储，格式为：
# {日期：[[区域，确诊人数],[区域，确诊人数],[区域，确诊人数],......],日期：[[区域，确诊人数],[区域，确诊人数],[区域，确诊人数],......],......}
# {2020-01-05：[[Afghanistan，0],[Angola，1],[Asia，2],......],2020-01-06：[[Afghanistan，0],[Angola，1],[Asia，2],......],......}
# 定义一个字典
data_dict={}
for line in content_list:
    date=line.split(',')[0]
    location=line.split(',')[1]
    total_cases=line.split(',')[4]

    # 如何判断字典里面有没有指定的key
    try:
        data_dict[date].append([location,total_cases])
    except KeyError:
        data_dict[date]=[]
        data_dict[date].append([location,total_cases])

# print(data_dict)

# 排序日期
sorted_date_list=sorted(data_dict.keys())
# print(sorted_date_list)

# 创建时间线对象
timeline=Timeline(
    {'theme':ThemeType.LIGHT}
)

for date in sorted_date_list:
    # 对每天的全球各地区的感染人数数据进行排序
    data_dict[date].sort(key=lambda element:element[1],reverse=True)
    # 取出当天感染人数最多的前10个地区
    date_data=data_dict[date][0:8]

    x_data=[]
    y_data=[]

    for number in date_data:
        x_data.append(number[0])    # x轴添加地区
        y_data.append(number[1])    # y轴添加感染人数

    # 构建柱状图
    bar=Bar()
    x_data.reverse()
    y_data.reverse()
    bar.add_xaxis(x_data)
    bar.add_yaxis('感染人数',y_data,label_opts=LabelOpts(position='right'))
    bar.reversal_axis()
    # 设置每一年图标的标题
    bar.set_global_opts(
        title_opts=TitleOpts(title=f'{date}日的全球感染人数前十的地区')
    )

    timeline.add(bar,date)

timeline.add_schema(
    play_interval=100,
    is_timeline_show=True,
    is_auto_play=True,
    is_loop_play=True
)

timeline.render('疫情动态数据.html')

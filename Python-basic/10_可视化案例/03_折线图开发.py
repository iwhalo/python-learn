#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：03_折线图开发.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 15:50 
@Function:
'''
import json
from pyecharts.charts import Line
from pyecharts.options import TitleOpts,LegendOpts,ToolboxOpts,VisualMapOpts,LabelOpts

f_world=open('全球每日感染数据.json', 'r', encoding='UTF-8')

# json转Python字典
world_dict=json.load(f_world)
# print(word_dict)

# 列表-记录数据中的日期
world_date=[]
# 列表-记录数据中每日感染人数
world_count=[]
for i in world_dict:
    # print(i)
    for j in i:
        # print(j)
        if j["name"]=="累计确诊":
            world_date.append(j['date'])
            world_count.append(j['value'])
            # print(f"日期：{j['date']}，累计确诊人数：{j['value']}")


line=Line()
line.add_xaxis(world_date)
line.add_yaxis('全球疫情数据每日展示',world_count,label_opts=LabelOpts(is_show=False))
# 全局配置
line.set_global_opts(
    title_opts=TitleOpts(is_show=True,title='全球每日确诊人数',pos_left="center",pos_bottom='1%'),
    legend_opts=LegendOpts(is_show=True),
    toolbox_opts=ToolboxOpts(is_show=True),
    visualmap_opts=VisualMapOpts(is_show=True)
)
line.render()
f_world.close()
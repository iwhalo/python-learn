#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_地图可视化的基本使用.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 16:44 
@Function:
'''
from pyecharts.charts import Map
from pyecharts.options import VisualMapOpts

map = Map()

# 省、市、自治区、行政区一定要与地图中展示的一致，否则数据不显示
data = [
    ("北京市", 199),
    ('上海市', 88),
    ('台湾省', 1999),
    ('香港特别行政区', 699),
    ('澳门特别行政区', 99999)
]

map.add('测试地图', data, 'china')

map.set_global_opts(
    visualmap_opts=VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        pieces=[
            {'min':1,'max':9,'label':'1-9人','color':'#CCFFFF'},
            {'min':10,'max':99,'label':'10-99人','color':'#FFFF99'},
            {'min':100,'max':499,'label':'100-499人','color':'#FFFF66'},
            {'min':500,'max':999,'label':'500-999人','color':'#FF6666'},
            {'min':1000,'max':9999,'label':'1000-9999人','color':'#CC3333'},
            {'min':10000,'label':'10000 以上','color':'#CCFFFF'},
        ]
    )
)

map.render()

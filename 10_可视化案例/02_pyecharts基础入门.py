#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：02_pyecharts基础入门.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 15:01 
@Function:
'''

# 导包
from pyecharts.charts import Line
from pyecharts.options import TitleOpts,LegendOpts,ToolboxOpts,VisualMapOpts

# 创建一个折线图对象
line=Line()

# 给折线图对象添加X轴数据
line.add_xaxis(["中国","美国","日本"])

# 给折线图对象添加Y轴数据
line.add_yaxis("GDP",[30,20,10])

# 通过render()方法，将代码生成为图像
# line.render()

# 设置全局配置项set_global_opts来设置
line.set_global_opts(
    title_opts=TitleOpts(is_show=True,title='GDP展示',pos_left='center',pos_bottom='1%'),
    legend_opts=LegendOpts(is_show=True),
    toolbox_opts=ToolboxOpts(is_show=True),
    visualmap_opts=VisualMapOpts(is_show=True),
)

line.render()

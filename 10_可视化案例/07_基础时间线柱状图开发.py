#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_基础时间线柱状图开发.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 19:08 
@Function:
'''
from pyecharts.charts import Bar,Timeline
from pyecharts.options import LabelOpts
from pyecharts.globals import ThemeType

bar1=Bar()
bar1.add_xaxis(['中国','美国','英国'])
bar1.add_yaxis('GDP',[50,30,20],label_opts=LabelOpts(position='right'))
bar1.reversal_axis()

bar2=Bar()
bar2.add_xaxis(['中国','美国','英国'])
bar2.add_yaxis('GDP',[70,50,30],label_opts=LabelOpts(position='right'))
bar2.reversal_axis()

# 创建时间线对象
# timeline=Timeline()
timeline=Timeline(
    {'theme':ThemeType.LIGHT}
)
# timeline对象添加bar柱状图
timeline.add(bar1,'2021年GDP')
timeline.add(bar2,'2022年GDP')

# 设置自动播放
timeline.add_schema(
    play_interval=1000,
    is_timeline_show=True,
    is_auto_play=True,
    is_loop_play=True
)

# 通过时间线绘图
timeline.render('基础柱状图-时间线.html')


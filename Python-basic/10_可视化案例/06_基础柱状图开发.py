#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_基础柱状图开发.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 18:18 
@Function:
'''

from pyecharts.charts import Bar
from pyecharts.options import LabelOpts

bar=Bar()

bar.add_xaxis(['中国','美国','英国'])
bar.add_yaxis('GDP',[30,20,10],label_opts=LabelOpts(
    position='right'
))

# 反转x和y轴
bar.reversal_axis()

bar.render('基础柱状图.html')

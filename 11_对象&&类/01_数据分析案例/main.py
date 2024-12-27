#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 16:56 
@Function: 面向对象，数据分析案例，主业务逻辑代码
'''

'''
实现步骤：
1.设计一个类，可以完成数据的封装
2.设计一个抽象类，定义文件读取的相关功能，并使用子类实现具体功能
3.读取文件，生产数据对象
4.进行数据需求的逻辑计算（计算每一天的销售额）
5.通过PyEcharts进行图形绘制
'''
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts.options import *

from data_define import Record
from file_define import TextFileReader, JsonFileReader

text_file_reader = TextFileReader('')
json_file_reader = JsonFileReader('')

jan_data: list[Record] = text_file_reader.read_data()
feb_data: list[Record] = text_file_reader.read_data()

# 将两个月份的数据合并为一个list来存储
all_data: list[Record] = jan_data + feb_data

# 开始进行数据计算
# 使用字典存储某一天的数据
# {“2011-01-01”：1534，“2011-01-02”：6666}
data_dict = {}
for record in all_data:
    if record.date in data_dict.keys():
        # 当前日期在字典里面已经有记录了，所以直接和已存在的key值进行累加即可
        data_dict[record.date] += record.money
    else:
        data_dict[record.date] = record.money

# print(data_dict)

# 可视化图表开发
bar=Bar(init_opts=InitOpts(theme=ThemeType.WHITE))
bar.add_xaxis(list(data_dict.keys()))
bar.add_yaxis('销售额',list(data_dict.values()),label_opts=LabelOpts(is_show=False))
bar.set_global_opts(
    title_opts=TitleOpts(title='每日销售额')
)

bar.render('每日销售额柱状图.html')
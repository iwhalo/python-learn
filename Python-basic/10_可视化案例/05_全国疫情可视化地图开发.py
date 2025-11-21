#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_全国疫情可视化地图开发.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 17:21 
@Function:
'''
import json

from pyecharts.charts import Map
from pyecharts.options import VisualMapOpts

f = open('China.txt', 'r', encoding='UTF-8')
data = f.read()
f.close()
data_dict = json.loads(data)
# print(data_dict)

province_data = data_dict['areas']
usercounts_data = data_dict['data']
currentuser_data = usercounts_data['现存确诊']
# print(province_data)
# print(usercounts_data)
# print(currentuser_data)

mapData_tuple = ()
mapData_list = []
province_index = 0
# currentuser_index = 0
while province_index <= len(province_data) - 1:
    if province_data[province_index] == '新疆':
        province_data[province_index] += '维吾尔自治区'
    elif province_data[province_index] == '西藏':
        province_data[province_index] += '自治区'
    elif province_data[province_index] == '宁夏':
        province_data[province_index] += '回族自治区'
    elif province_data[province_index] == '内蒙古':
        province_data[province_index] += '自治区'
    elif province_data[province_index] == '广西':
        province_data[province_index] += '壮族自治区'
    elif province_data[province_index] in ['香港''澳门']:
        province_data[province_index] += '特别行政区'
    else:
        province_data[province_index] += '省'

    # 组装每个省份和确诊人数为元组
    mapData_tuple = (province_data[province_index], currentuser_data[province_index])
    # print(mapData_tuple)
    # 组装各个省的数据都封装入列表内
    mapData_list.append(mapData_tuple)
    # print(mapData_list)

    # mapData_dict.update({province_data[province_index]: currentuser_data[province_index]})
    province_index += 1

# print(mapData_dict)
# print(mapData_tuple)
print(mapData_list)

map = Map()
map.add("全国各省疫情数据", mapData_list, 'china')
map.set_global_opts(
    visualmap_opts=VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        pieces=[
            {'min':1,'max':99,'label':'1-99人','color':'#CCFFFF'},
            {'min':100,'max':999,'label':'100-999人','color':'#FFFF99'},
            {'min':1000,'max':4999,'label':'1000-4999人','color':'#FF9966'},
            {'min':5000,'max':9999,'label':'5000-9999人','color':'#FF6666'},
            {'min':10000,'max':99999,'label':'10000-99999人','color':'#CC3333'},
            {'min':10000,'label':'10000+','color':'#990033'},
        ]
    )
)
map.render('全国各省疫情数据地图.html')

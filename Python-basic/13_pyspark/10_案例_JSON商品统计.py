#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：10_案例_JSON商品统计.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 16:15 
@Function: 元成练习案例：JSOW商品统计
需求：
1.各个城市销售额排名，从大到小
2.全部城市，有娜些商品类别在售卖
3.北京市有哪些商品类别在售卖
'''
import json
import os

# 1、构建执行环境入口对象
from pyspark import *

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"

conf = SparkConf().setMaster("local[*]").setAppName("test_spark")
sc = SparkContext(conf=conf)

# TODO 需求1：城市销售额排名
# 1.1 读取文件得到RDD
file_rdd = sc.textFile("./orders.txt")
print(file_rdd.collect())

# 1.2取出一个json字符串
json_str_add = file_rdd.flatMap(lambda x: x.split("|"))
print(json_str_add.collect())

# 1.3 将一个个JSON字符串转换为字典
dict_rdd = json_str_add.map(lambda x: json.loads(x))
print(dict_rdd.collect())

# 1.4 取出城市和销售额数据
# （城市，销售额）
# tup_rdd = dict_rdd.map(lambda x: (x['areaName'], x['money']))
city_with_money_rdd = dict_rdd.map(lambda x: (x['areaName'], int(x['money'])))
print(city_with_money_rdd.collect())

# 1.5 按城市分组，按销售额聚合
city_result_rdd = city_with_money_rdd.reduceByKey(lambda a, b: a + b)
print(city_result_rdd.collect())

# 1.6 按销售额聚合结果进行排序
result1_rdd = city_result_rdd.sortBy(lambda x: x[1], ascending=False, numPartitions=1)
print("需求1的结果是：", result1_rdd.collect())

# TODO 需求2：全部城市有哪些商品类别在售卖
category_rdd = dict_rdd.map(lambda x: x["category"]).distinct()
print("需求2的结果是：", category_rdd.collect())

# TODO 需求3：北京市有哪些商品在售卖
beijing_data_rdd = dict_rdd.filter(lambda x: x["areaName"] == "北京")
result3_rdd = beijing_data_rdd.map(lambda x: x["category"]).distinct()
print("需求3的结果是：", result3_rdd.collect())

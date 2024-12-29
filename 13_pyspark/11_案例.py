#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 17:19 
@Function: 演示将RDD输出位Python对象
'''

import os

# 1、构建执行环境入口对象
from pyspark import *

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"

conf = SparkConf().setMaster("local[*]").setAppName("test_spark")
sc = SparkContext(conf=conf)

rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9])

# collect算子，输出RDD为list对象
print(rdd)  # ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:289
rdd_list: list = rdd.collect()
print(rdd_list)
print(type(rdd_list))  # <class 'list'>

# reduce算子，对RDD进行两两聚合
num = rdd.reduce(lambda a, b: a + b)
print(num)

# take算子，取出RDD前N个元素，组成list返回
take_list = rdd.take(3)
print(take_list)

# count算子，统计rdd内有多少条数据，返回值为数字
count = rdd.count()
print(count)

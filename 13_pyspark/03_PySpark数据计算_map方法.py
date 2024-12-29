#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 1:04
# @Author  : fuqingyun
# @File    : 03_PySpark数据计算_map方法.py
# @Description : 演示RDD的map成员方法使用

import os

from pyspark import SparkConf, SparkContext

os.environ['PYSPARK_PYTHON'] = 'D:\Python\Python311\python.exe'

conf = SparkConf().setMaster('local[*]').setAppName('test_spark')
sc = SparkContext(conf=conf)

# 准备一个RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])


# 通过map方法将全部数据都乘以10
def func(data):
    return data * 10


rdd2 = rdd.map(func)
print(rdd2.collect())  # [10, 20, 30, 40, 50]

rdd3 = rdd.map(lambda x: x * 10).map(lambda x: x + 5)
print(rdd3.collect())

# (T) - > U
# (T) -> T

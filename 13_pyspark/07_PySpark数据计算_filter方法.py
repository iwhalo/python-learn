#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：07_PySpark数据计算_filter方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 15:09 
@Function: 演示RDD的filter成员方法的使用
'''

import os

from pyspark import *

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"

conf = SparkConf().setMaster("local[*]").setAppName("test_spark")
sc = SparkContext(conf=conf)

# 准备一个RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])

# 对RDD数据进行过滤
rdd2 = rdd.filter(lambda num: num % 2 == 0)
print(rdd2.collect())

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_PySpark数据计算_distinct方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 16:00 
@Function: 演示RDD的distinct成员方法的使用
'''

from pyspark import *
import os

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"
conf = SparkConf().setMaster("local[*]").setAppName("test_spark")
sc = SparkContext(conf=conf)

# 准备对RDD数据进行去重
rdd = sc.parallelize([1, 2, 3, 3, 5, 5, 5, 6, 7, 8, 9, ])
rdd2 = rdd.distinct()
print(rdd2.collect())

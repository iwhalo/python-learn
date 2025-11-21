#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_PySpark数据计算_reduceBySpark方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 14:37 
@Function: 演示RDD的reduceByKey成员方法的使用
'''

import os

from pyspark import SparkConf, SparkContext

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"

conf = SparkConf().setMaster("local[*]").setAppName("test_spark")
sc = SparkContext(conf=conf)

# 准备一个RDD
rdd = sc.parallelize([("男", 99), ("女", 88), ("男", 77), ("女", 66)])
# 需求：求男生、女生两个组的成绩之和
rdd2 = rdd.reduceByKey(lambda a, b: a + b)
print(rdd2.collect())

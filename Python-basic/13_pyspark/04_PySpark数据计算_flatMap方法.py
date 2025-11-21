#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_PySpark数据计算_flatMap方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 14:23 
@Function: 演示RDDLatMap成员方法的使用
'''

import os

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local[*]').setAppName('test_spark')
sc = SparkContext(conf=conf)
rdd = sc.parallelize(["itheima itcast 666", "itheima itcast itcast", "python itheima"])

# 需求：将RDD数据里面的一个个单词提取出来
# rdd2=rdd.map(lambda x:x.split(" "))   # [['itheima', 'itcast', '666'], ['itheima', 'itcast', 'itcast'], ['python', 'itheima']]
rdd2 = rdd.flatMap(
    lambda x: x.split(" "))  # ['itheima', 'itcast', '666', 'itheima', 'itcast', 'itcast', 'python', 'itheima']
print(rdd2.collect())

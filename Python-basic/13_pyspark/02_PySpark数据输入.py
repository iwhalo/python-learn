#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 0:37
# @Author  : fuqingyun
# @File    : 02_PySpark数据输入.py
# @Description : 演示通过PySpark代码加载数据，即数据输入

from pyspark import SparkConf,SparkContext

conf=SparkConf().setMaster('local[*]').setAppName('test_spark')
sc=SparkContext(conf=conf)

# 通过parallelize方法将Python对象加载到Spark内，成为RDD对象
rdd1=sc.parallelize([1,2,3,4,5])
rdd2=sc.parallelize((1,2,3,4,5))
rdd3=sc.parallelize("abcdefg")
rdd4=sc.parallelize({1,2,3,4,5})
rdd5=sc.parallelize({'key1':'value1','key2':'value2','key3':'value3'})

# 如果要查看RDD里面有什么内容，需要collect()方法
print(rdd1.collect())
print(rdd2.collect())
print(rdd3.collect())
print(rdd4.collect())
print(rdd5.collect())

# 用textFile方法，读取文件数据加载到Spark内成为RDD对象
rdd=sc.textFile(r'G:\pycharmProjects\python-learn\13_pyspark\rdd_text')

print(rdd.collect())

sc.stop()

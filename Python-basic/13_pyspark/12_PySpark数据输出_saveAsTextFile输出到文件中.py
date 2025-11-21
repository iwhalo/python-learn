#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：12_PySpark数据输出_saveAsTextFile输出到文件中.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 17:35 
@Function: 演示将RDD输出到文件中
'''
import os
from pyspark import *

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"
'''
调用保存文件的算子，需要配置Hadoop依赖
·下载Hadoop安装包
http://archive.apache.org/dist/hadoop/common/hadoop-3.0.0/hadoop-3.0.0.tar.gz
·解压到电脑任意位置
·在Python代码中使用os模块配置：os.environ['HADOOP HOME]=HADOOP解压文件夹路径'
·下载winutils.exe,并放入Hadoop解压文件夹的bin目录内
https://raw.githubusercontent.com/steveloughran/winutils/master/hadoop-3.0.0/bin/winutils.exe
·下载hadoop.dl,并放入：C:Windows/System32文件夹内
https://raw.githubusercontent.com/steveloughran/winutils/master/hadoop-3.0.0/bin/hadoop.dll
'''
os.environ["HADOOP_PYTHON"] = "E:\PycharmProjects\softs\hadoop-3.4.1"

conf = SparkConf().setMaster("local[*]").setAppName("test_spark")

# 修改RDD分区为1个
# 方式1，SparkConfi对象设置属性全局并行度为1：
conf.set("spark.default.parallelism", "1")

sc = SparkContext(conf=conf)

# 方式2，创建RDD的时候设置(parallelize方法传入numSlices参数为1)
rdd1 = sc.parallelize([1, 2, 3, 4, 5])

rdd2 = sc.parallelize([("Hello", 3), ("Spark", 5), ("Hi", 7)])

rdd3 = sc.parallelize([[1, 3, 5], [6, 7, 9], [11, 13, 11]])

# 输出到文件中
rdd1.saveAsTextFile("./output1")
rdd2.saveAsTextFile("./output2")
rdd3.saveAsTextFile("./output3")

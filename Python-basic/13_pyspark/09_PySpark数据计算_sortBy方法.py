#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：09_PySpark数据计算_sortBy方法.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 16:08 
@Function:
'''
import os

# 1、构建执行环境入口对象
from pyspark import *

os.environ["PYSPARK_PYTHON"] = "D:\Python\Python311\python.exe"

conf = SparkConf().setMaster("local[*]").setAppName("test_spark")
sc = SparkContext(conf=conf)

# 2、读取数据文件
rdd = sc.textFile('./美国独立宣言.txt')

# 3、取出全部单词
word_rdd = rdd.flatMap(lambda x: x.split(" "))
print(word_rdd.collect())
# 4、将所有单词都转换成二元元组，单词为key，value设置为1
word_with_one_rdd = word_rdd.map(lambda word: (word, 1))
print(word_with_one_rdd.collect())
# 5、分组求和
result_rdd = word_with_one_rdd.reduceByKey(lambda a, b: a + b)
print(result_rdd.collect())

final_rdd = result_rdd.sortBy(lambda x: x[1], ascending=False, numPartitions=1)

# 6、打印输出结果
print(final_rdd.collect())

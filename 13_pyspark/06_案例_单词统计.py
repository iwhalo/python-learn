#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_案例_单词统计.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/30 14:45 
@Function: 完成练习案例：单词计数统计
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
result = word_with_one_rdd.reduceByKey(lambda a, b: a + b)
# 6、打印输出结果
print(result.collect())

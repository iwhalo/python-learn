#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：file_define.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 17:03 
@Function: 和文件相关的类定义
'''
import json

from data_define import Record


# 先定义一个抽象类用来做顶层设计，确定有哪些功能需要实现
class FileReader:

    def read_data(self) -> list[Record]:
        '''读取文件的数据，将读到的每一条数据都转换为Record对象，将所有对象都封装到List内返回即可'''
        pass


class TextFileReader(FileReader):

    def __init__(self, path):
        self.path = path  # 定义成员变量，记录文件路径

    # 复写（实现抽象方法）父类的方法
    def read_data(self) -> list[Record]:
        f = open(self.path, 'r', encoding='UTF-8')

        # 定义一个list容器
        record_list = []

        for line in f.readlines():
            line = line.strip()  # 消除读取到的每一行数据中的换行符\n
            # print(line)
            data_list = line.split(',')
            # 将读到的每一条数据都转换为Record对象
            record = Record(data_list[0], data_list[1], int(data_list[2]), data_list[3])
            #           #将所有对象都封装到List
            record_list.append(record)
        f.close()
        return record_list


class JsonFileReader(FileReader):

    def __init__(self, path):
        self.path = path

    def read_data(self) -> list[Record]:
        f = open(self.path, 'r', encoding='UTF-8')
        record_list = []
        for line in f.readlines():
            data_dict = json.loads(line)
            record = Record(data_dict['date'], data_dict['order_id'], data_dict['money'], data_dict['province'])
            record_list.append(record)
        f.close()
        return record_list


# 测试一下
if __name__ == '__main__':
    list1 = TextFileReader(
        r'E:\PycharmProjects\pythonProject_study\python-learn\10_可视化案例\full_data.csv').read_data()
    list2 = JsonFileReader(r'E:\PycharmProjects\pythonProject_study\python-learn\10_可视化案例\全球每日感染数据.json').read_data()

    print(list1)
    print(list2)
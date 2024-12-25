#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：file_util.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 11:40 
@Function:
'''


def print_file_info(file_name):
    """
    功能：将给定路径的文件内容输出到控制台
    :param file_name: 即将读取的文件路径
    :return: None
    """
    fr = None
    try:
        fr = open(file_name, 'r', encoding='UTF-8')
        print('文件的全部内容如下：\n')
        print(fr.read())
    except Exception as e:
        print(f"程序出现异常了，原因是：{e}")
    finally:
        if fr:      # 若果变量是None，表示False，如果有任何内容，就是True
            fr.close()

if __name__ == '__main__':
    print_file_info('D:/bill.txt')


def append_to_file(file_name, data):
    """
    功能：将指定的数据追加到指定的文件中
    :param file_name: 指定的文件路径
    :param data: 指定的数据
    :return: None
    """
    fw = open(file_name, 'a', encoding='UTF-8')
    fw.write(data)
    fw.write('\n')
    fw.close()

if __name__ == '__main__':
    append_to_file('D:/bill7777.txt','test')

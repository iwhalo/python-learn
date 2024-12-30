#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_递归.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 21:00 
@Function:
'''

import os


def test_os():
    """演示OS模块的三个基础方法"""
    print(os.listdir("D:/test"))
    print(os.path.isdir("D:/test/a"))
    print(os.path.exists("D:/test"))


def get_files_recursion_from_dir(path):
    """"""
    print(f"当前判断的文件夹是：{path}")
    file_list = []
    if os.path.exists(path):
        for f in os.listdir(path):
            new_path = path + "/" + f
            if os.path.isdir(new_path):
                # 进入到这里，表明这个目录是文件夹不是文件
                get_files_recursion_from_dir(new_path)
            else:
                file_list.append(new_path)
    else:
        print(f"指定的目录{path}，不存在")
        return []

    return file_list


if __name__ == '__main__':
    # test_os()
    get_files_recursion_from_dir("D:/test")

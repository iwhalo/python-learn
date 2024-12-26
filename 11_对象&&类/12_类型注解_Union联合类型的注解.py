#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：12_类型注解_Union联合类型的注解.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/27 16:10 
@Function:
'''

from typing import Union

my_list: list[Union[int, str]] = [1, 2, 'itheima', 'itcast']
my_dict: dict[str, Union[str, int]] = {"name": '周杰伦', "age": 18}


def func(data: Union[int, str]) -> Union[int, str]:
    pass


func()

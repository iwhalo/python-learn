#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：str_util.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 11:11 
@Function:
'''

def str_reverse(s):
    """
    功能是将字符串反转
    :param s: 将被反转的字符串
    :return: 反转后的字符串
    """
    index = len(s) - 1
    new_str = ''
    while index >= 0:
        new_str += s[index]
        index -= 1
    return new_str
    # 方法2：通过序列切片来反转
    # return s[::-1]


if __name__ == '__main__':
    a = str_reverse('abc')
    print(a)


def sub_str(s,x,y):
    """
    功能是按照给定的下标完成给定字符串的切片
    :param s: 即将被切片的字符串
    :param x: 切片的开始下标
    :param y: 切片的结束下标
    :return: 切片完成后的字符串
    """
    new_str=''
    while x<=y:
        new_str+=s[x]
        x+=1
    return new_str

    # 方法2：通过序列切片
    # return s[x,y]

if __name__ == '__main__':
    b = sub_str('abcdefghikjlmbyn', 3, 5)
    print(b)
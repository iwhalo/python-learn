#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：06_多线程编程_传参.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 11:46 
@Function:
'''

import threading
import time


def sing(msg):
    while True:
        print(msg)
        time.sleep(1)


def dance(msg):
    while True:
        print(msg)
        time.sleep(1)


if __name__ == '__main__':
    # sing()
    # dance()

    sing_thread = threading.Thread(target=sing, args=('我在唱歌',))
    dance_thread = threading.Thread(target=dance, kwargs={'msg': '我在跳舞'})

    # 让线程去干活
    sing_thread.start()
    dance_thread.start()

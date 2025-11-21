#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：05_多线程编程.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 11:35 
@Function: 演示多线程编程的使用
'''
import threading
import time


def sing():
    while True:
        print("我在唱歌")
        time.sleep(1)


def dance():
    while True:
        print("我在跳舞")
        time.sleep(1)


if __name__ == '__main__':
    # sing()
    # dance()

    sing_thread = threading.Thread(target=sing)
    dance_thread = threading.Thread(target=dance)

    # 让线程去干活
    sing_thread.start()
    dance_thread.start()

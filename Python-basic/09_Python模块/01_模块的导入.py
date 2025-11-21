#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/26 1:13
# @Author  : fuqingyun
# @File    : 01_模块的导入.py
# @Description :


import time

print('nihao')
time.sleep(1)
print('wohao')

from time import sleep
sleep(1)

from time import *
sleep(1)
time_ns()

import time as t
t.sleep(1)

from time import sleep as sl
sl(3)

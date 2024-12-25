#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：04_案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/26 11:47 
@Function:
'''

import my_utils.str_util
from my_utils import file_util

# 将下面的字符串反转
test_str='豫章故郡，洪都新府。星分翼轸(zhěn)，地接衡庐。襟三江而带五湖，控蛮荆而引瓯（ōu）越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃(fān)之榻。雄州雾列，俊采星驰，台隍(huáng)枕夷夏之交，宾主尽东南之美。都督阎公之雅望，棨(qǐ )戟遥临；宇文新州之懿(yì)范，襜(chān )帷(wéi)暂驻。十旬休假，胜友如云；千里逢迎，高朋满座。腾蛟起凤，孟学士之词宗；紫电清霜，王将军之武库。家君作宰，路出名区；童子何知，躬逢胜饯。'
reverse_str=my_utils.str_util.str_reverse(test_str)
print(reverse_str)

# 将翻转后的字符串按照下标10到20进行切片
split_str=my_utils.str_util.sub_str(reverse_str,10,20)
print(split_str)

print('======================')

# 打印文件fr_text.txt内的全部内容
file_util.print_file_info('../09_Python模块/fr_text.txt')

file_util.append_to_file('../09_Python模块/fw_text.txt','abcdef')


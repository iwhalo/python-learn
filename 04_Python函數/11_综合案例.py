#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：11_综合案例.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2023/1/20 11:15 
@Function:
'''


user_account = 0
name=None

name=input("请输入您的姓名：")

# 定义查询函数
def account_query(show_header):
    if show_header:
        print("-------------------------查询余额-----------------------")
    print(f"{name}，您好，您的余额为： {user_account} 元")

# 定义存款函数
def account_save(money):
    print("------------------------存款---------------------------")
    global user_account
    user_account += money
    print(f"{name}，您好，您存款{money}元成功。")

    # 调用account_query函数查询余额
    # 为了不打印account_query函数第一行，加个判断条件show_header=False
    account_query(False)

# 定义取款函数
def account_withdraw(money):
    print("------------------------取款---------------------------")
    global user_account
    user_account -= money_withdraw
    print(f"{name}，您好，您取款{money}元成功。")

    account_query(False)

# 定义菜单选择
def user_operation():
    print("-------------------------主菜单-----------------------")
    print(f"{name}，您好，欢迎来到黑马银行ATM。请选择操作：")
    print("查询余额\t输入【1】")
    print("存款\t输入【2】")
    print("取款\t输入【3】")
    print("退出\t输入【4】")
    return  input("请输入您的选择：")

# 设置无限循环，确保程序不退出
while True:
    Keyboard_input=user_operation()

    if Keyboard_input == "1":
        account_query(True)
        continue
    elif Keyboard_input == "2":
        money_save = int(input(f"{name}，您好，请输入您的存款金额："))
        account_save(money_save)
        continue
    elif Keyboard_input == "3":
        money_withdraw = int(input(f"{name}，您好，请输入您的取款金额："))
        account_withdraw(money_withdraw)
        continue

    elif Keyboard_input == "4":
        print("请取走您的银行卡！")
        break

#     global user_account_inial
#     if user_select == 1:
#         account_check(user_account_inial)
#
#     elif user_select == 2:
#         account_save(user_account_inial)
#         account_check(user_account_inial)
#
#     elif user_select == 3:
#         account_withdraw()
#         account_check(user_account_inial)
#
#     elif user_select == 4:
#         print("请取走您的银行卡！")
#
# while True:
#     user_operation(user_select_button)
#     continue

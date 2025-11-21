#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：08_Socket编程_客户端开发.py
@IDE     ：PyCharm 
@Author  ：fuqingyun
@Date    ：2024/12/31 17:30 
@Function:
'''

import socket

# 创建socket对象

socket_client = socket.socket()

# 连接服务器
socket_client.connect(("localhost", 8866))

# 发送消息
while True:
    # 发送消息
    msg = input("请输入要给服务端发送的消息：")
    if msg == 'exit':
        break

    socket_client.send(msg.encode("UTF-8"))

    # 接收返回的消息
    recv_data = socket_client.recv(1024)
    print(f"服务端回复的消息是：{recv_data.decode('UTF-8')}")

socket_client.close()

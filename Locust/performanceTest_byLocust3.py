#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/22 18:04
# @Author  : fuqingyun
# @File    : performanceTest_byLocust3.py
# @Description : locust执行负载测试——测试途中增加测试用户
import os

# 1.首先是安装locust
# pip install locust

# 2.导包使用，需要知道locust有哪些常用的函数和类需要导入
from locust import HttpUser, task, events, TaskSet, SequentialTaskSet, tag,between
'''
Httpuser，这是一个类，这个类是用来生成用于攻击被测服务器的虚拟用户的，此类在实例化时创建一个*client*属性self.client替requests该属性是一个支持的HTTP客户端用于在请求之间保持用户会话，相当于不用手动传递cookie。

TaskSet，这是一个类，这个类定义用户执行的一组任务，用法就是自己另外定义一个测试任务类去继承这个类，自己定义的类下的方法就是需要执行的任务。

SequentialTaskSet，这是一个类，这个类继承了TaskSet这个类，主要区别在于你定义的测试任务类继承如果继承的是TaskSet，下面的测试任务不是按代码从上到下顺序执行的，如果继承的是SequentialTaskSet就是按代码从上到下执行的测试任务。

task，这是一个方法，是声明测试任务的装饰器，就是在上面定义好的测试类下的方法加上@task这个装饰器，那么被装饰的方法就是测试任务。

tag，这是一个方法，给定标记名标记测试任务的装饰器@tag，加在测试任务上可以限制仅执行被标记的任务或排除执行标记的任务，在启动locust使用时，加--tags参数或-T，排除使用-E。

between，这是一个方法，产生一个随机等待时间，模拟用户发出不同请求间的间隔时间。
'''

class TestTask(TaskSet):
    @task(5)
    def task1(self):
        print('task1')

    @task(3)
    def task2(self):
        print('task2')

    @task(2)
    def task3(self):
        print('task3')


# 4.定义测试计划类，继承HttpUser
class TestPlan(HttpUser):
    host='http://127.0.0.1:8080'
    tasks = [TestTask]
    wait_time = between(1,3)

'''
host是项目的地址

tasks是一个任务列表，要执行的任务都放在这个列表

wait_time是每个任务间的间隔时间，根据实际场景而定
'''

# 5.1有图形界面的启动，在终端执行命令
#  locust -f .\performanceTest_byLocust.py

# 5.2无图形界面启动
'''
locust -f performanceTest_byLocust.py --headless -u 1 -r 1 -t 60s
参数说明：
--headless 无图形界面
-u 设置总的虚拟用户数
-r 设置每秒启动的用户数
-t 设置测试执行时间，到时停止，时间格式300s, 20m, 3h, 1h30m

注意默认情况下，-t参数的时间到了Locust会立即停止您的任务，如果还有任务没有跑完可以加上-s/--stop-timeout参数再跑一会儿。
'''
# locust -f .\performanceTest_byLocust.py --headless -u 1 -r 1 -t 60s -s 10s

# 测试途中加负载
'''
step1：在控制台使用命令启动脚本
         locust -f .\performanceTest_byLocust3.py        
step2：执行后locust会在本地开一个端口8089的访问地址，本地访问该地址localhost:8089进入主界面，启动测试
step3：启动测试后在终端界面，按w添加1个用户或W加10个。按s删除1个或S移除10个。
'''


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/22 18:04
# @Author  : fuqingyun
# @File    : performanceTest_byLocust.py
# @Description : @task装饰器用来声明测试任务
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

# 3.根据自身业务定义测试任务类
# 定义测试任务类1
class TestTask1(TaskSet):
    # on_start、on_stop都是以用户维度来执行的，即一个用户执行一次
    def on_stop(self):
        print('任务开始了')

    def on_stop(self):
        print('任务结束了')

    @task
    def task1(self):
        pass

    @task
    def task2(self):
        pass

# 如有需要，继续定义测试任务类2
class TestTask2(TaskSet):
    pass

'''
estTask1,TestTask2就是你定义的测试任务类，需要继承TaskSet或SequentialTaskSet；

被@task装饰器装饰的方法task1、task2就是虚拟用户执行的测试任务

另外locust还提供了每个测试任务类执行的前置后置操作on_start方法在测试任务执行前执行，on_stop在测试任务执行完成后执行，需要注意的是这里的前置后置操作是针对每一个执行用户的，即有多少的用户执行测试任务前置后置方法就会执行多少次。
'''

# 4.定义测试计划类，继承HttpUser
class TestPlan(HttpUser):
    host='http://127.0.0.1:8080'
    tasks = [TestTask1, TestTask2]
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

# 将启动命令写在脚本中方便启动
if __name__=='__main__':
    os.system('locust -f .\performanceTest_byLocust.py')
    # os.system('locust -f .\performanceTest_byLocust.py --stop-timeout 20s')
    # os.system('locust -f .\performanceTest_byLocust.py --headless -u 100 -r 10 -t 60s -s 10s')
    # os.system('locust -f .\performanceTest_byLocust.py --headless -u 10 -r 2 -t 60s')


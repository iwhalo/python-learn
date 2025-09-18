import time
from functools import wraps

import requests


class RateLimiter:
    """请求频率限制器"""
    def __init__(self,calls_limit,time_period):
        """
        初始化限流器
        :param calls_limit：时间段内允许的最大请求数
        :param time_period：时间段长度（秒）
        """
        self.calls_limit=calls_limit
        self.time_period=time_period
        self.timestamps=[]

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            # 检查是否超出频率限制
            now=time.time()
            # 清理过期的时间戳
            self.timestamps=[t for t in self.timestamps if now-t<self.time_period]

            # 检查是否超出限制
            if len(self.timestamps)>=self.calls_limit:
                # 计算需要等待的时间
                oldest_call=min(self.timestamps)
                sleep_time=self.time_period-(now-oldest_call)
                if sleep_time>0:
                    print(f"频率限制：等待{sleep_time:.2f}秒")
                    time.sleep(sleep_time)


            # 记录本次调用时间
            self.timestamps.append(time.time())
            return func(*args,**kwargs)

        return wrapper

# 使用示例：限制每分钟最多三十个请求
@RateLimiter(calls_limit=30,time_period=60)
def limited_request(url):
    return requests.get(url)

# 请求节流示例
def throttled_requests(urls,requests_per_second=5):
    """按指定频率发送请求"""
    delay=1.0/requests_per_second
    results=[]

    for url in urls:
        start=time.time()
        response=requests.get(url)
        results.append(response)

        # 计算需要等待的时间
        process_time=time.time()-start
        wait_time=delay-process_time
        if wait_time>0:
            time.sleep(wait_time)

    return results

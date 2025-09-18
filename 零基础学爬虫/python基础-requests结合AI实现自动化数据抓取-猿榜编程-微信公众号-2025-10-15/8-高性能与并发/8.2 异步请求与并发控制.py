import concurrent.futures
import time
from functools import partial

import requests


def fetch_url(url,session,timeout=10):
    """发送单个请求，并计时"""
    start=time.time()
    try:
        with session.get(url,timeout=timeout) as response:
            data=response.text
            return {
                'url':url,
                'data':data[:30]+'...' if data else None,   # 截断显示
                'status':response.status_code,
                'time':time.time()-start
            }
    except Exception as e:
        return {
            'url':url,
            'error':str(e),
            'time':time.time()-start
        }

def fetch_all(urls,max_workers=10,timeout=10):
    """并发获取多个URL"""
    with requests.Session() as session:
        # 设置会话参数
        session.headers.update({'User-Agent':'Mozilla/5.0'})

        # 创建部分应用函数，固定会话参数
        func=partial(fetch_url,session=session,timeout=timeout)

        # 使用线程池并发执行
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_url={executor.submit(func,url): url for url in urls}

            # 收集结果
            results=[]
            for future in concurrent.futures.as_completed(future_to_url):
                results.append(future.result())

        return results

# 使用示例
urls=[
    'https://httpbin.org/delay/1',
    'https://httpbin.org/delay/2',
    'https://httpbin.org/delay/3'
]

results=fetch_all(urls,max_workers=5)
for result in results:
    print(f"{result.get('url')}：{result.get('status','ERROR')} in {result.get('time'):.2f}s")

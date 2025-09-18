import time

import requests
from tornado.httpclient import HTTPError


def resumable(url,method='GET',max_retries=3,**kwargs):
    """
    可中断恢复的请求函数，支持网络中断后自动恢复
    """
    retry_count=0
    last_exception=None
    response=None

    # 获取已下载内容的位置（如果有）
    if 'headers' not in kwargs:
        kwargs['headers']={}

    # 支持流式请求
    stream=kwargs.get('stream',False)

    while retry_count<max_retries:
        try:
            if response is not None and stream:
                # 如果是流式请求 且 之前有进度，添加断点续传头
                downloaded=sum(len(chunk) for chunk in response.iter_content(chunk_size=1))
                if downloaded>0:
                    kwargs['headers']['Range']=f'bytes={downloaded}-'

            response=requests.request(method,url,**kwargs)

            # 成功获取响应
            if response.status_code in [200,206]:   # OK 或 Partial Content
                return response

            # 适当处理其他状态码
            response.raise_for_status()

        except (ConnectionError,TimeoutError) as e:
            print(f"连接中断：{e}，尝试恢复...")
            retry_count+=1
            last_exception=e
            time.sleep(2**retry_count)  # 指数退避
        except HTTPError as e:
            # 如果是客户端错误，不再重试
            if 400 <= e.response.status_code <500:
                print(f"客户端错误：{e.response.status_code}")
                raise
            # 服务器错误则重试
            retry_count+=1
            last_exception=e
            time.sleep(2**retry_count)


    # 超过最大重试次数
    if last_exception:
        raise last_exception

    return None

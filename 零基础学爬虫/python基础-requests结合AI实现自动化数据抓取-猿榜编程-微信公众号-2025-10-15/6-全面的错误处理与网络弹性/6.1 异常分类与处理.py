import requests

from requests.exceptions import (
    RequestException,  # 所有异常的基类
    ConnectionError,   # 连接错误
    HTTPError,         # HTTP 错误状态码
    Timeout,           # 请求超时
    TooManyRedirects,  # 重定向过多
    URLRequired,       # URL 缺失
    InvalidURL,        # URL 无效
    InvalidHeader,     # 请求头无效
    InvalidSchema,     # 协议无效
    MissingSchema,     # 协议缺失
    ChunkedEncodingError,  # 分块编码错误
    ContentDecodingError,   # 内容解码错误
    StreamConsumedError,    # 流内容已消费错误
    RetryError,             # 重试失败
    UnrewindableBodyError,  # 请求体无法回退
    FileModeWarning,        # 文件模式警告
    ConnectTimeout,         # 连接超时
    ReadTimeout,            # 读取超时
)

def safe_request(method, url, **kwargs):
    """安全的请求包装函数，处理所有可能的异常"""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # 抛出 HTTP 错误
        return response
    except ConnectionError as e:
        print(f"网络连接错误：{e}")
    except Timeout as e:
        print(f"请求超时：{e}")
    except TooManyRedirects as e:
        print(f"重定向过多：{e}")
    except HTTPError as e:
        print(f"HTTP 错误：{e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"状态码：{e.response.status_code}")
            print(f"响应内容：{e.response.text[:200]}...")  # 显示前 200 个字符
    except RequestException as e:
        print(f"请求异常：{e}")
    return None

# 使用示例
response = safe_request('GET', 'https://httpbin.org/status/500')
if response:
    print("请求成功")
else:
    print("请求失败")
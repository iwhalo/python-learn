import logging
from http.client import HTTPConnection

import requests

# 设置HTTP连接的调试级别
HTTPConnection.debuglevel=1

# 配置日志
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log=logging.getLogger('urllib3')
requests_log.setLevel(logging.DEBUG)
requests_log.propagate=True

# 发送请求，将显示详细的HTTP请求和响应xx
r=requests.get('https://httpbin.org/get')



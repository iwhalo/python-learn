import requests

# 自定义适配器配置
from requests.adapters import HTTPAdapter


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', 5.0)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        return super().send(request, **kwargs)


# 使用自定义适配器
session = requests.Session()
adapter = TimeoutHTTPAdapter(timeout=10.0, max_retries=3)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 所有请求将默认使用 10 秒超时和 3 次重试
r = session.get('https://httpbin.org/delay/9')  # 应该成功完成
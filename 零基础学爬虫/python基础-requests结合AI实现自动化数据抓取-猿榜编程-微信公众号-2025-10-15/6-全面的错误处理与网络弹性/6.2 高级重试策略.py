import random
import requests
from requests import RequestException
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# 自定义退避策略 - 兼容性版本
class CustomRetry(Retry):
    """自定义退避时间计算"""

    def get_backoff_time(self):
        # 使用安全的方式获取当前重试次数
        # 在新版本中，重试次数信息可能存储在不同的属性中
        try:
            # 尝试多种可能的属性名
            if hasattr(self, 'history'):
                retry_count = len(self.history)
            elif hasattr(self, '_retry_count'):
                retry_count = self._retry_count
            else:
                # 如果都找不到，使用默认值
                retry_count = 0
        except:
            retry_count = 0

        # 计算退避时间
        backoff = min(self.backoff_max, self.backoff_factor * (2 ** retry_count))
        # 增加随机抖动（jitter），防止请求风暴
        jitter = random.uniform(0, 0.1 * backoff)
        return backoff + jitter

    def increment(self, method=None, url=None, response=None, error=None, _pool=None, _stacktrace=None):
        """在重试前执行自定义操作"""
        # 修正：使用 response.status 而不是 response.status_code
        if response and 500 <= response.status <= 599:
            print(f"服务器错误（{response.status}），准备重试...")
        elif response and response.status == 429:
            print(f"速率限制（429），准备重试...")
        elif error:
            print(f"发生错误: {type(error).__name__}，准备重试...")

        return super().increment(method, url, response, error, _pool, _stacktrace)


# 配置高级重试策略
retry_strategy = CustomRetry(
    total=5,  # 最大重试次数
    backoff_factor=0.5,  # 退避系数
    status_forcelist=[429, 500, 502, 503, 504],  # 触发重试的状态码
    allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"],  # 允许重试的方法
    raise_on_status=False,  # 修改为False，通过异常处理来控制
)

# 应用重试策略
adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

# 使用示例
try:
    response = session.get("https://httpbin.org/status/503", timeout=(3.05, 27))
    print(f"成功获得响应：{response.status_code}")
except RequestException as e:
    print(f"所有重试失败：{e}")
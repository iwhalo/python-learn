import urllib.request
import random

from django.db.models.expressions import result

# 常见浏览器User-Agent列表
user_agents = [
    # Chrome 浏览器 User-Agent ---Windows 平台
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # Chrome 浏览器 User-Agent ---macOS 平台
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # Chrome 浏览器 User-Agent ---Linux 平台
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # Firefox 浏览器 User-Agent ---Windows 平台
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    # Firefox 浏览器 User-Agent ---macOS 平台
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    # Firefox 浏览器 User-Agent ---Linux 平台
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    # Safari 浏览器 User-Agent ---macOS 平台
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    # Safari 浏览器 User-Agent ---iOS 平台
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    # Edge 浏览器 User-Agent
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    # 移动设备 User-Agent ---Android Chrome
    'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    # 移动设备 User-Agent ---iPhone Safari
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1'
]


# 随机选择一个User-Agent
user_agent=random.choice(user_agents)
print(f'使用User-Agent: {user_agent}')

# 创建请求
req=urllib.request.Request(
    url='http://httpbin.org/post',
    headers={'User-Agent':user_agent}
)

# 发送请求
res=urllib.request.urlopen(req)
result=res.read().decode('utf-8')
print(result)


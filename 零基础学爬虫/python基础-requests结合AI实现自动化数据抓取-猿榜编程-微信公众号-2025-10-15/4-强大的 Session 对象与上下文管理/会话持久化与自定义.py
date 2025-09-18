import requests

# 创建自定义会话
session = requests.Session()

# 会话级别的参数设置
session.headers.update({'User-Agent': 'MyApp/1.0.0'})
session.auth = ('user', 'pass')
session.proxies = {'http': 'http://proxy.example.com:8080'}
session.verify = '/path/to/certfile'  # HTTPS 证书验证
session.cert = ('/path/to/client.cert', '/path/to/client.key')  # 客户端证书
session.cookies.set('session_cookie', 'value')  # 预设 Cookie

# 会话级默认参数与请求级参数合并
r = session.get('https://httpbin.org/cookies',
                params={'q': 'test'},  # 这个参数仅用于此次请求
                timeout=5)  # 这个超时设置仅用于此次请求
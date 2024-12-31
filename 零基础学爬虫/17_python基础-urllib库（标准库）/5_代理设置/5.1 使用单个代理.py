import urllib.request

# 代理服务器地址
proxy_handler=urllib.request.ProxyHandler(
    {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080',
    }
)

# 创建opener
opener=urllib.request.build_opener(proxy_handler)

# 安装opener
urllib.request.install_opener(opener)

# 发送请求
try:
    response=urllib.request.urlopen('http://www.baidu.com')
    print(response.read().encode('utf-8'))
except urllib.error.URLError as e:
    print(f'代理连接失败：{e.reason}')
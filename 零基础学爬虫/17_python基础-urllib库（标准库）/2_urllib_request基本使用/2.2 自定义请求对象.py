import urllib.request

# 创建Request对象
req=urllib.request.Request('https://www.douyu.com/')

# 添加请求头
req.add_header(
    'User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
)
req.add_header(
    'Referer','https://www.douyu.com/'
)

# 发送请求
response=urllib.request.urlopen(req)

# 读取响应内容
html=response.read().decode('utf-8')

# 打印请求方法和完整url
print(f'请求方法：{req.get_method()}')
print(f'完整url：{req.full_url}')

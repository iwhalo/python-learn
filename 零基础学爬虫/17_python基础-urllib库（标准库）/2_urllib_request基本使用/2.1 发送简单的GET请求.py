import urllib.request

# 发送GET请求并获取响应
response=urllib.request.urlopen('https://www.douyu.com/')

# 读取响应内容
html=response.read()

# 打印响应内容（前300个字符）
print(html[:300])

# 获取响应状态码
print(f'状态码：{response.status}')

# 获取响应头信息
print(f'响应头：{response.getheaders()}')

# 获取特定的响应头
print(f'Content-Type:{response.getheader('Content-Type')}')


# 获取实际url（处理重定向后）
print(f'实际URL：{response.url}')
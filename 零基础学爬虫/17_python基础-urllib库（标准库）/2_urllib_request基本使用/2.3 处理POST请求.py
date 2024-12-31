import urllib.request

import urllib.parse

# 准备post数据
data={
    'username':'admin',
    'password':'123456'
}

# 将数据编码为字节
data=urllib.parse.urlencode(data).encode('utf-8')

# 创建Request对象，指定POST方法
req=urllib.request.Request(
    url='https://www.douyu.com/',
    data=data,
    method='POST'
)

# 添加请求头
req.add_header('Content-Type','application/x-www-form-urlencoded')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0')

# 发送请求
response=urllib.request.urlopen(req)

# 读取响应内容
result=response.read().decode('utf-8')
print(result)
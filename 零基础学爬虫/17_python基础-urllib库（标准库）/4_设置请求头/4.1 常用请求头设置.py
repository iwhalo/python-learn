import urllib.request

# 创建请求对象
req=urllib.request.Request('http://httpbin.org/post')

# 设置常用请求头
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    'Content-Type':'application/json',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection':'keep-alive',
    'Host':'httpbin.org',
    'Referer':'http://httpbin.org/post',
    'Cache-Control':'max-age=0',
    'DNT':'1'# Do Not Track
}

# 批量添加请求头
for key,value in headers.items():
    req.add_header(key,value)

# 获取所有请求头
print(req.headers)

# 发送请求
response=urllib.request.urlopen(req)
html=response.read().decode('utf-8')
print(html[:100])
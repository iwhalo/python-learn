import urllib.request
import urllib.parse

# 表单数据
form_data={
    'username':'admin',
    'password':'123',
    'remember':'true'
}

# 编码表单数据
data=urllib.parse.urlencode(form_data).encode('utf-8')

# 创建请求
req=urllib.request.Request(
    url='https://httpbin.org/post',
    data=data,
)

# 添加表单请求头
req.add_header('Content-Type','application/x-www-form-urlencoded')

# 发送请求
response=urllib.request.urlopen(req)
result=response.read().decode('utf-8')
print(result)
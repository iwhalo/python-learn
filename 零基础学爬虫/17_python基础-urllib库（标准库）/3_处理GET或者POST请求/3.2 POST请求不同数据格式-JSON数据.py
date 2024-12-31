import urllib.request
import json

from django.db.models.expressions import result

# json数据
json_data={
    'username':'admin',
    'password':'123456',
    'info':{
        'age':25,
        'city':'北京'
    }
}

# 编码JSON数据
data=json.dumps(json_data).encode('utf-8')

# 创建请求
req=urllib.request.Request(
    url='https://httpbin.org/post',
    data=data
)

# 添加JSON请求头
req.add_header('Content-Type','application/json')

# 发送请求
response=urllib.request.urlopen(req)
result=response.read().decode('utf-8')
print(result)